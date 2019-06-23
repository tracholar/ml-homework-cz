#coding:utf-8
from data_utils import *

ss = StanfordSentiment()

print ss.tokens()
print ss.sentences()[0]
print ss.rejectProb()
trainSet = ss.getTrainSentences()
devSet = ss.getDevSentences()
testSet = ss.getTestSentences()
print trainSet[0]