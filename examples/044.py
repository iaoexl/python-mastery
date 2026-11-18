#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
两个 3 行 3 列的矩阵，实现其对应位置的数据相加，并返回一个新矩阵：
'''

X = [[11, 12, 13],
     [14, 15, 16],
     [17, 18, 19]]

Y = [[21, 22, 23],
     [24, 25, 26],
     [27, 28, 29]]

result = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]

# 迭代输出行
for i in range(len(X)):
    # 迭代输出列
    for j in range(len(X[0])):
        result[i][j] = X[i][j] + Y[i][j]

for r in result:
    print(r)
