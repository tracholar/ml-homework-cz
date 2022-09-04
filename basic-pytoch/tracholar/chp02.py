# coding:utf-8
import torch
import numpy as np

t1 = torch.from_numpy(np.random.rand(10, 1))
t2 = torch.ones_like(t1)
t3 = torch.rand_like(t1)

t4 = torch.concat([t1, t2, t3], dim=1)

print(t1.T @ t2)
print(torch.matmul(t1.T, t2))

print(t1.mean())
print(t1.add_(5))
print(t1.numpy())
