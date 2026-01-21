from src.gpt import GPT, GPTConfig
from src.dataloader import DataLoader
import tiktoken
import math
import torch
import time

total_batch_size = 524288
B, T = 16, 1024
max_lr = 6e-4
min_lr = max_lr * 0.1
warmup_steps = 10
max_steps = 50

grad_accum_steps = total_batch_size // (B * T)

def get_lr(it):
    if it < warmup_steps:
        return max_lr * (it+1) / warmup_steps

    elif it > max_steps:
        return min_lr

    else:
        decay_ratio = (it -warmup_steps) / (max_steps - warmup_steps)
        assert 0 <= decay_ratio <= 1
        coeff = 0.5 * (1.0 + math.cos(math.pi * decay_ratio))
        return min_lr + coeff * (max_lr - min_lr)
