#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
python操作
'''

# 斐波那契数列
n = 0
n = int (input("输入您要的斐波那契数列数位："))
def fib(n):
    if n == 1:
        return [1]
    if n == 2:
        return [1, 1]
    fibs = [1, 1]
    for i in range(2, n):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

print(fib(n))