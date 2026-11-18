#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
统计 1 到 100 之和。
'''

tmp = 0
for i in range(1,100+1):
    tmp += i
print('1+2+…+99+100=%d' %tmp)
