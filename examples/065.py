#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
输入3个数a,b,c，按大小顺序输出。
'''
a=[]
for i in range(3):
    a.append(input("请输入%d个数字：" % (i+1)))
a.sort()
print (a)
