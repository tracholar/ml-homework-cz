import numpy as np

n_sample = 10000
dim = 10
x = np.random.randn(n_sample, dim)
w = np.random.rand(dim)
b = np.random.rand(n_sample)

y = np.dot(x, w) + b

with open('data.csv', 'w') as f:
    for xi, yi in zip(x, y):
        f.write(','.join(f'{i:.4f}' for i in xi) + f',{yi:.2f}\n')