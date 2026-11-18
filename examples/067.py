#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
输入数组，最大的与第一个元素交换，最小的与最后一个元素交换，输出数组。
'''
import numpy as np
a=[]
n = int(input("输入数组位数：\n"))
for i in range(0,n+1):
    a.append(input("输入第%d个数字:" % (i+1)))

print ("原数组为：%s" %a)
# 最小的放到最后
min = min(a)
a.remove(min)
a.append(min)
# 最大的放到最前面
max = max(a)
a.remove(max)
a.insert(0,max)
print ("现数组为：%s" %a)
