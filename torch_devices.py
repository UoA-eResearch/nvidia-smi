#!/usr/bin/env python3
import torch
import time
from pprint import pprint

s = time.time()
print(f"PyTorch version: {torch.__version__}")
print("PyTorch build information:")
pprint(torch.__config__.show())
print("PyTorch CUDA availability:", torch.cuda.is_available())

# List physical devices (GPUs)
print("PyTorch CUDA devices:")
for i in range(torch.cuda.device_count()):
    device = torch.cuda.get_device_name(i)
    print(f"GPU {i}: {device}")

print(f"Took {round(time.time() - s)}s")
