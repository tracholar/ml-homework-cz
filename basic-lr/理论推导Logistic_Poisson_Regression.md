

# 1.Logistics Regression

- **使用 -1 ，1 作为label**

$$
log\frac{(p(y=1|x))}{(p(y=0|x))}=W^Tx+b\\
\\
\\

p(y=1|x)+p(y=0|x)=1\\
$$

可得：
$$
p(y=1|x)=\frac {1}{1+e^{-W^Tx}}\\
p(y=0|x)=\frac {1}{1+e^{W^Tx}}
$$
联合起来可得：

​              
$$
p(y|x)=\frac{1}{1+e^{-yW^Tx}},y\in \{0,1\}
$$
使用最大似然函数可推得损失函数为：
$$
min\quad -log\ p(y|x)=log(1+e^{-yW^Tx})
$$
梯度下降法求解:
$$
w=w-alpha*\frac{(e^{-yW^Tx})*(-y*x)}{(1+e^{-yW^Tx})}
$$

```python
            	"""
                y_w_x=np.exp(-y * W^T * x)
                """
                y_w_x=np.exp(-y[j]*np.dot(self.weights.T,tmp_x))
                """
                grad=(1+y_w_x)*(-y*x)/(1+y_w_x)
                """
                grad=y_w_x*(-y[j]*tmp_x)/(1+y_w_x)
                self.weights=self.weights-self.learning_rate*grad
```





- **使用 1,0作为标签**

有概率：
$$
p(y|x)=（\frac{1}{1+e^{-W^Tx}})^y（\frac{1}{1+e^{W^Tx}})^{1-y},y\in \{0,1\}
$$
有**损失函数**：
$$
min \quad ylog(1+e^{-W^Tx})+(1-y)log(1+e^{W^Tx})
$$
**Q:对数几率的理论解释？概率比值的对数服从线性分布？**



# 2.Poisson Regression

[泊松分布博客](http://www.cnblogs.com/kemaswill/p/3440780.html)

[泊松分布wikipedia](https://zh.wikipedia.org/zh-hans/%E6%B3%8A%E6%9D%BE%E5%9B%9E%E5%BD%92)

- 假设离散随机变量$Y$服从如下概率分布函数：

$$
P(y)=\frac{\lambda^ye^{-\lambda}}{y!}
$$

​	其中$\lambda>0,y=0,1,2,.....$则称$Y$服从泊松分布。

​	有如下性质：

​	a.$E[Y]=\lambda$

​	b.$Var[Y]=\lambda$

​	c.$Y_1\sim Poisson(\lambda_1),Y_2\sim Poisson(\lambda_2)$则 $Y=Y_1+Y_2\sim Poisson(\lambda_1+\lambda_2)$

- 泊松回归

对于$\lambda=W^Tx+b$，或者$\lambda=e^{W^Tx+b}$有：
$$
P(Y=y|\lambda)=\frac{\lambda^ye^{-\lambda}}{y!}
$$
那么在已知数据$\{(x_1,y_1),(x_2,y_2),...,(x_n,y_n)\}$时，可以对参数$W$和$b$进行求解估计。



- 损失函数

​       使用最大似然估计对泊松回归进行求解：
$$
max\ \ \ log(\prod _{i=0}^n\frac{\lambda_i^{y_i}e^{-\lambda_i}}{{y_i}!})
$$
​      则可以得到相应的**`损失函数`**为：                            
$$
min  -ylog(\lambda)+\lambda+\sum_{k=1}^ylogk
$$


- 梯度下降法求解($\lambda=e^{W^Tx+b}$)

$$
W\ =W- \alpha  f^\prime(W)\\
f=-y ({W^Tx+b})+e^{W^Tx+b}+\sum_{k=1}^ylogk\\
f^\prime(W)=-yx+e^{W^Tx+b}\cdot x
$$

Q: 损失函数是不是再用一个Log的好。

```python
				"""
                grad=-y*x+np.exp(w^Tx)+x
                """
         grad=-tmp_x*y[j]+np.exp(np.dot(self.weights.T,tmp_x))*tmp_x        				        
                """
                w=w-alpha * grad(w)
                """
                self.weights-=self.learning_rate*grad
```









