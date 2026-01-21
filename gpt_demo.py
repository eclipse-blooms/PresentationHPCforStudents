from src.training import *
device = "cuda:2"

model = GPT(GPTConfig(vocab_size=50304))
model.to(device)

model = torch.compile(model)

optimizer = torch.optim.AdamW(model.parameters(), lr=max_lr)
enc = tiktoken.get_encoding('gpt2')
train_loader = DataLoader(B, T, 1, 1)


start = time.time()
for i in range(100):
    #with torch.no_grad():
    x, _ = train_loader.next_batch()
    x = x.to(device)
    logits, loss = model(x)

torch.cuda.synchronize()
end = time.time()
total = int((end - start) * 1000)
print(f"{total}ms elapsed")