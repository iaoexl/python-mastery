#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
对10个数进行排序。
'''
print('输入请10个数字')
a=[]
for n in range(10):
    m = n + 1
    a.append(int(input("请输入第%d个数字："% m))) # append附加函数
a.sort() # sort排序函数
print(a)
