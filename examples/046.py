#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
求输入数字的平方，如果平方运算后小于 50 则退出。
'''

def SQ(x):
    return x * x
again = 1
while again:
    num = int(input('input num:'))
    print("n*n=%d" % (SQ(num)))
    if SQ(num) >= 50:
        again = True
    else:
        again = False
