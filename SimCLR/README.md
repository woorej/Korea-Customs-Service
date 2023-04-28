# Reference
Github: https://github.com/Spijkervet/SimCLR

### Training ResNet encoder:
Simply run the following to pre-train a ResNet encoder using SimCLR on the CIFAR-10 dataset:
```
python main.py --dataset CIFAR10
```

### Distributed Training
- DDP P2P  
With distributed data parallel (DDP) training:
```
CUDA_VISIBLE_DEVICES=0 python main.py --nodes 2 --nr 0
CUDA_VISIBLE_DEVICES=1 python main.py --nodes 2 --nr 1
CUDA_VISIBLE_DEVICES=2 python main.py --nodes 2 --nr 2
CUDA_VISIBLE_DEVICES=N python main.py --nodes 2 --nr 3
```
- DDP Nccl  
```
python3 -m torch.distributed.run --nproc_per_node=4 main_nccl_ddp.py
```
