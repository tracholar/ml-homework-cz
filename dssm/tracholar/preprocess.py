#coding:utf-8
import pickle
import jieba
import random

fp = open('toutiao_cat_data.txt')

words = set()
train = []
test = []
n = 0
for line in fp:
    row = line.strip().split('_!_')
    title, tags = (row[3], row[4].split(','))
    title_words = jieba.cut(title)
    for w in jieba.cut(title):
        words.add(w)
    for t in tags:
        words.add(t)
    if random.random()<0.9:
        data = train
    else:
        data = test
    data.append({"title": title_words, "tags" : tags})
    n += 1
    if n % 1000 == 0:
        print '\rprocess', n ,'rows',


word2idx = {v:i for i,v in enumerate(words)}
for data in [train, test]:
    for d in data:
        d['title'] = [word2idx[w] for w in d['title']]
        d['tags'] = [word2idx[w] for w in d['tags']]


data = {
    "wordcnt" : len(words),
    "word2idx" : word2idx,
    "train" : train,
    "test" : test
}
fp = open("data.pkl", "wb")
pickle.dump(data, fp)
fp.close()