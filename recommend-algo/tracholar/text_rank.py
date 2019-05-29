#coding:utf-8
"""Text Rank Algorithm"""
import re
import networkx as nx
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def article_dataset():
    data = open('./data/article.xml').read()
    return re.findall(r'<article>(.+?)</article>', data, re.S|re.M)

def text_rank(txt):
    sentenses = [s.strip() for s in re.split(r'。|\n|\.', txt.strip()) if len(s) > 5]
    vct = TfidfVectorizer(tokenizer=lambda x: jieba.cut(x))
    X = vct.fit_transform(sentenses)
    similar = cosine_similarity(X)
    G = nx.Graph()
    for i in range(len(sentenses)):
        for j in range(i+1, len(sentenses)):
            G.add_weighted_edges_from([(i, j, similar[i, j])])
    node_weight = nx.pagerank(G)
    m = 0
    mw = 0
    for i, w in node_weight.items():
        if w > mw:
            m = i
            mw = w
    return sentenses[m]


if __name__ == '__main__':
    for a in article_dataset():
        print text_rank(a)
