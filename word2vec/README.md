## Word2Vec实现
- 参考cs224d(现在叫cs224n) assignment1 实现word2vec


## 思考题
1. 为什么要做word2vec? word2vec解决的是什么问题?请联系几个实际例子加以说明?
2. word2vec与之前基于SVD的方法有啥区别和相同的?
3. word2vec与基于语言模型的word embedding的相同点和不同点?
4. word2vec与主题模型的相同点和不同点?
5. 找一个语料,利用word2vec(现有的工具)得到词向量,并对词向量进行聚类,请可视化你的结果
6. 利用语料:[今日头条](https://github.com/fate233/toutiao-text-classfication-dataset),实现 onehot+SVM 文本分类和基于词向量的文本分类,对比一下二者的效果
    1. 有人说onehot+SVM可以看做一个特殊的word2vec,你觉得对吗?请详细说明
7. word2vec是一个多分类问题,负采样可以看做一个二分类的问题,请联系推荐点击率预估场景,请解释这种观点?
8. word2vec的问题有哪些?有哪些解决方法?


## 实现
- [tracholar](tracholar/)
- [getstart](getstart/)
