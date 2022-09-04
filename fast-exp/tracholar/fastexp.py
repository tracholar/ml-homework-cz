import numpy as np

x = np.linspace(0, 10, 1001)
y = np.exp(x)
for z, expz in zip(x, y):
    print('{:6f},'.format(expz))


