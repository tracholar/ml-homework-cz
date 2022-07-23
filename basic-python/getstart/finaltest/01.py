# coding:utf-8
# 绘制分形图：科赫曲线和分形三角形
import matplotlib.pyplot as plt
from matplotlib import collections
from math import cos, sin, pi


def gen_koch(start_point, line_args, depth=0):
    if depth >= 5:
        return []

    x1, y1 = start_point
    theta, d = line_args

    x2 = x1 + 1.0/3*d * cos(theta)
    y2 = y1 + 1.0/3*d * sin(theta)

    x3 = x1 + 2.0/3*d * cos(theta)
    y3 = y1 + 2.0/3*d * sin(theta)

    x4 = x1 + d * cos(theta)
    y4 = y1 + d * sin(theta)

    




fig = plt.figure(figsize=(8, 8))
ax = plt.gca()
ax.set_axis_off()

lines = [(0, 0), (0.5, 0.732), (1, 0)]
lines = list(zip(lines[:-1], lines[1:]))
print(lines)

line_seg = collections.LineCollection(lines)
ax.add_collection(line_seg, autolim=True)

plt.savefig('img/01.svg')

