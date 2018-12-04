# Poission Regression 
如下公式为poission Regression相关公式，由概率密度函数推导得到最大似然函数，后转换为最小对数似然函数进行参数估计，并推导得到梯度更新公式。

- 公式
p(y|x;\theta)=\frac{\lambda ^{y}e^{-\lambda }}{y!}，其中\lambda=e^{\theta^{T}x}

- 概率函数
p(Y|X;\theta) = \frac{\lambda^y}{y!}e^{-\lambda}=\frac{e^{y\theta^{T}Xe^{-\theta^{T}X}}}{y!}

- 极大似然函数如下：  
L(\theta|X,Y) = p(y_1,...,y_m|X_1,...,X_m;\theta)=\frac{\lambda^y}{y!}e^{-\lambda}=\frac{e^{y\theta^{T}Xe^{-\theta^{T}X}}}{y!}

- log似然函数：
log(\theta|X,Y) = \sum_{1}^{m} y_i \theta^Tx_i-e^{\theta^T x_i}-log(y_i!)

- 转换为求最小值：
-log(\theta|X,Y) = -\sum_{1}^{m} y_i \theta^Tx_i-e^{\theta^T x_i}-log(y_i!)  
- 因为损失函数中最后一项与参数无关，因此损失函数可以保留前两项：
-log(\theta|X,Y) = -\sum_{1}^{m} y_i \theta^Tx_i-e^{\theta^T x_i}

- 对参数求导得到最终的更新梯度：
\frac{\partial loss}{\partial \theta} = -\sum_{1}^{m} y_i * x_i-e^{\theta^T x_i} * x_i
- 转换为矩阵相乘形式如下：
\frac{\partial loss}{\partial \theta} = - (sum(X.T * Y, axis=1) - sum(X.T * e^(\theta^T x_i),axis=1)
