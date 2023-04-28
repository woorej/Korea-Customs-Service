# Reference
Github: https://github.com/Spijkervet/SimCLR
# Run on CPU or Single GPU
```
python3 main.py
```

### Distributed Training
- DDP P2P(Working on RTX3090 but Not working on RTX4090)
below command suppose : you have one node(computer) and 4 GPUs
```
CUDA_VISIBLE_DEVICES=0 python3 main.py --nodes 4 --nr 0
CUDA_VISIBLE_DEVICES=1 python3 main.py --nodes 4 --nr 1
CUDA_VISIBLE_DEVICES=2 python3 main.py --nodes 4 --nr 2
CUDA_VISIBLE_DEVICES=3 python3 main.py --nodes 4 --nr 3
```
- DDP Nccl(Working on RTX3090 and RTX4090)
```
python3 -m torch.distributed.run --nproc_per_node=4 main_nccl_ddp.py
```
