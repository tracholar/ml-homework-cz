#coding:utf-8


def load_dic():
    words = set()
    for line in open('./data/CoreNatureDictionary.mini.txt') \
            .read().split('\n'):
        if line is not None:
            row = line.split('\t')
            if len(row) > 2:
                words.add(row[0])
    return words

dic = load_dic()

def segment(text):
    ws = []
    i = 0
    while i < len(text):
        best_len = 1
        best_w = text[i]
        for j in range(i+1,len(text) + 1):
            w = text[i:j]
            if w in dic:
                if best_len < j - i:
                    best_len = j - i
                    best_w = w

        ws.append(best_w)
        i = i + best_len

    return ws

print ','.join(segment('工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作'))

