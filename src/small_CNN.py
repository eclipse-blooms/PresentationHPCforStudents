import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
import torchvision
from torchvision import datasets, transforms
import time
from tqdm import tqdm

in_channels   = 3
num_classes   = 10
num_workers   = 8
batch_size    = 1024 #this is pretty large for the actual model we use here, but not unreasonable in other usecases
num_epochs    = 15
learning_rate = 0.005

transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])
train_data = datasets.CIFAR10(root='data', train=True, transform=transform,download=True)
train_loader = DataLoader(train_data, batch_size=batch_size, num_workers=num_workers, shuffle=True)

train_data = datasets.CIFAR10(
    root='data',
    train=True,
    transform=transform,
    download=True
)

class Net(nn.Module):
    def __init__(self, num_classes, dropout=0.2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=5, stride=1, padding=0),
            nn.BatchNorm2d(32),
            nn.Dropout2d(dropout),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=0),
            nn.BatchNorm2d(64),
            nn.Dropout2d(dropout),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Flatten(),
            nn.Linear(64 * 5 * 5, 400),
            nn.BatchNorm1d(400),
            nn.Dropout(dropout),
            nn.ReLU(),
            nn.Linear(400, 100),
            nn.BatchNorm1d(100),
            nn.Dropout(dropout),
            nn.ReLU(),
            nn.Linear(100, num_classes))

    def forward(self, x):
        return self.net(x)