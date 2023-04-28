import os
import torch
import torchvision
import torch.distributed as dist
from torchvision.models import resnet50
import torchvision.transforms as transforms
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler



# DDP
distributed = False

if 'WORLD_SIZE' in os.environ:
    distributed = int(os.environ['WORLD_SIZE']) > 1
    # Total gpu number
    world_size = int(os.getenv('WORLD_SIZE', 1))


# 1. initialize process group
if distributed :
        # local_rank 값 구하기
        local_rank = int(os.getenv('LOCAL_RANK', -1))
        torch.distributed.init_process_group(backend='nccl',
                                            init_method='env://', 
                                            rank=local_rank, 
                                            world_size=world_size)
        
        torch.cuda.set_device(local_rank)
else :
    world_size = 1
    local_rank = 0

print(f"DDP:{distributed}, local_rank:{local_rank} GPU:{torch.cuda.current_device()}, Total_device:{world_size}")

dataset_dir="./data"
os.makedirs(dataset_dir, exist_ok=True)

transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor()
])

train_dataset = torchvision.datasets.CIFAR10(
            dataset_dir,
            train=True,
            download=True,
            transform=transform
)

test_dataset = torchvision.datasets.CIFAR10(
            dataset_dir,
            train=False,
            download=True,
            transform=transform
)


if distributed :
    train_sampler = torch.utils.data.distributed.DistributedSampler(
        train_dataset, num_replicas=world_size, rank=local_rank, shuffle=True)
else :
    print("train Sampler not initialized")
    train_sampler = None

workers = 4
batch_size = 100
train_loader = torch.utils.data.DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=(train_sampler is None),
    drop_last=True,
    pin_memory=True,
    num_workers=workers,
    sampler=train_sampler
)

test_loader = torch.utils.data.DataLoader(
            test_dataset, 
            batch_size=batch_size, 
            shuffle=False, 
            num_workers=workers)

# define model
model = resnet50(weights="IMAGENET1K_V2")
model.to(local_rank)

# 손실 함수 및 옵티마이저 설정
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# DDP
if distributed :
    model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)
    model = DDP(model, device_ids=[local_rank])

#학습 루프
num_epochs = 5
for epoch in range(num_epochs):
        model.train()
        #train_sampler.set_epoch(epoch)
        for step, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(local_rank), labels.to(local_rank)
            optimizer.zero_grad()
            outputs = model(inputs)

            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            #print(f"Before All Reduce-GPU:{local_rank}, loss:{loss}")
            if dist.is_available() and dist.is_initialized():
                loss = loss.data.clone()
                dist.all_reduce(loss.div_(dist.get_world_size()))
            #print(f"After All Reduce-GPU:{local_rank}, loss:{loss}")

            if local_rank==0 and step % 50 == 0: 
                print(f"Step [{step}/{len(train_loader)}]\t Loss: {loss.item()}")

        # 테스트
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(local_rank), labels.to(local_rank)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        if local_rank==0 :
            print(f"Epoch [{epoch+1}/{num_epochs}], Accuracy: {100 * correct / total:.2f}%")