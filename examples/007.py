#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
将一个列表的数据复制到另一个列表中。
'''

a = [1,2,3]
b = a[:]
c = a[::-1]
print('原数据为：',a)
print('复制的数据为：',b)
print('取反的数据为：',c)
