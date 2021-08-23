# coding:utf-8
import numpy as np


def gen_batch(bath_size=128, dim=1024, dense_ratio=0.1):
    """
    如果用批量梯度下降, batch_size 请设置为100000, 且只获取一次
    :param bath_size:
    :param dim:
    :param dense_ratio:
    :return: (w, X, y)
    """
    np.random.seed(2018)  # 保证每次都是相同的w
    w = np.random.randn(dim) / np.sqrt(dim)
    mask = (np.random.rand(dim) < (1 - dense_ratio)).astype(int)
    w = w * mask

    np.random.seed(None)  # 保证每次的数据都是不同的
    X = np.random.randn(bath_size, dim)
    y = (np.dot(X, w) + np.random.rand(X.shape[0]) * 0.1 > 0).astype(int) * 2 - 1
    return w, X, y


def _sigmiod(t):
    return 1. / (1. + np.exp(-t))


def loss_function(w, X, y):
    # TODO 返回损失、梯度、海森矩阵
    y_hat = _sigmiod(X.dot(w))
    loss = - np.sum(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat)) / len(y)
    grad = X.T.dot(_sigmiod(X.dot(w)) - y) / len(X)
    g = grad.reshape((-1, 1))
    Hessian = np.matmul(g, g.T)
    return loss, grad, Hessian


def numeric_gradient(f, w, epsilon=1e-4):
    assert len(w.shape) == 1, "w必须是向量"

    g = np.zeros(w.shape)
    for i in range(w.shape[0]):
        dw = np.zeros(w.shape)
        dw[i] = epsilon
        df = f(w + dw) - f(w - dw)
        g[i] = df / epsilon / 2
    return g


if __name__ == '__main__':
    w0, X, y = gen_batch(bath_size=10000)
    w = np.random.rand(w0.shape[0]) / w0.shape[0]
    f = lambda x: loss_function(x, X, y)[0]
    loss, g0 = loss_function(w, X, y)
    g1 = numeric_gradient(f, w)
    print(np.linalg.norm(g0 - g1))
    assert np.linalg.norm(g0 - g1) < 1e-4
