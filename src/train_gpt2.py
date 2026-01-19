import torch
import tiktoken
import time
import math
import os
from torch.distributed import init_process_group, destroy_process_group
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.distributed as dist

from src.gpt import GPT, GPTConfig
from src.dataloader import DataLoader

assert torch.cuda.is_available()
torch.manual_seed(42)
torch.cuda.manual_seed(42)
torch.set_float32_matmul_precision('high')


total_batch_size = 524288
B, T = 32, 1024
max_lr = 6e-4
min_lr = max_lr * 0.1
warmup_steps = 10
max_steps = 50



ddp_rank = int(os.environ['RANK'])
ddp_local_rank = int(os.environ['LOCAL_RANK'])
ddp_world_size = int(os.environ['WORLD_SIZE'])
init_process_group(backend='nccl', rank=ddp_rank, world_size=ddp_world_size)
device = f'cuda:{ddp_local_rank}'
torch.cuda.set_device(device)
master_process = ddp_rank == 0
assert total_batch_size % (B * T * ddp_world_size) == 0
grad_accum_steps = total_batch_size // (B * T * ddp_world_size)



model = GPT(GPTConfig(vocab_size=50304))

model.to(device)

model = torch.compile(model)

optimizer = torch.optim.AdamW(model.parameters(), lr=max_lr)
enc = tiktoken.get_encoding('gpt2')
train_loader = DataLoader(B, T, ddp_rank, ddp_world_size)



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

def train_one_microbatch(step):
    x, y = train_loader.next_batch()
    x, y = x.to(device), y.to(device)

    with torch.autocast(device_type='cuda', dtype=torch.bfloat16):
        logits, loss = model(x, y)
    loss = loss / grad_accum_steps
    model.require_backward_grad_sync = (step == grad_accum_steps-1)
    loss.backward()
    return loss.detach()

def train(it):
    optimizer.zero_grad()
    avg_loss = 0.0

    for micro_step in range(grad_accum_steps):
        avg_loss += train_one_microbatch(micro_step)

    lr = get_lr(it)
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr

    avg_loss = avg_loss / grad_accum_steps
    avg_loss = dist.all_reduce(avg_loss, op=dist.ReduceOp.AVG)
    norm = torch.nn.utils.clip_grad_norm(model.parameters(), 1.0)
    optimizer.step()
    return avg_loss, norm

if master_process:
    start = time.time()
    avg_batch_time = 0
    for i in range(max_steps):
        start_batch = time.time()

        loss, norm = train(i)

        torch.cuda.synchronize()
        end_batch = time.time()
        batch_time = int((end_batch - start_batch) * 1000)
        print(f"step {i+1}, loss: {loss}, {batch_time}ms elapsed")
        avg_batch_time += batch_time
    end = time.time()
    print(f"{int((end-start)*1000)}ms elapsed, {avg_batch_time / max_steps}ms avg batch time")
else:
    for i in range(max_steps):
        loss, norm = train(i)
destroy_process_group()
