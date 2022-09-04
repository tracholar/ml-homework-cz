# coding:utf-8
import torch

x = torch.ones(5)  # input tensor
y = torch.zeros(3)  # expected output
w = torch.randn(5, 3, requires_grad=True)
b = torch.randn(3, requires_grad=True)
z = torch.matmul(x, w)+b

loss = torch.nn.functional.binary_cross_entropy_with_logits(z, y)

print(z.grad_fn)
print(w.grad)

loss.backward()
print(w.grad)