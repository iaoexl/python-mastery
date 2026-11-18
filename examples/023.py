#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 打印出如下图案（菱形）:
'''
先把图形分成两部分来看待，前三行一个规律，后四行一个规律，利用双重for循环，第一层控制行，第二层控制列。
'''

for i in range(1,4):
    print(' ' * (4-i),end="")
    for j in range(1,2*i):
        print("*",end="")
    print()

for i in range(4,0,-1):
    print(' ' * (4-i),end="")
    for j in range(1,2*i):
        print("*",end="")
    print()
