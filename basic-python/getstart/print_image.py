# coding:utf-8
import numpy as np
from PIL import Image


def read_img(path='cat.jpeg'):
    img = Image.open(path).convert('L')
    img.thumbnail([100, 100])
    return np.asarray(img)


def print_img(data):
    # TODO 将图片打印成字符画
    # 图片数据data可以看做一个2维list
    # 即每个元素都是一个list，代表图片每一行的像素值，取值范围在0-255之间
    #
    # Tips:
    # 你需要做的是便利这个2维list，对像素值超过阈值的打印一个+号，
    # 对像素值小于阈值的打印一个·号
    # 最终你将看到一个蒙娜丽莎的字符画
    # 打印不换行的方法是添加一个end参数， print('hello', end='')
    for line in data:
        for x in line:
            if x< 180:
                print('+', end='')
            else:
                print('·', end='')
        print()

print_img(read_img())