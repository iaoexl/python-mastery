#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
四个数字组成无重复三位数
'''

# 有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？
ad = 0
print("数组分别是")
for i in range(1,5):
    for j in range(1,5):
        for k in range(1,5):
            if (i != j)and(i != k)and(j != k):
                print(i,j,k)
                ad += 1
print('共有',ad,'组')