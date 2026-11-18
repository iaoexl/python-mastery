#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
数字比较。
'''
a = int(input("a:"))
b = int(input("b:"))
if a > b:
    print('%d 大于 %d' % (a,b))
elif a == b:
    print('%d 等于 %d' % (a,b))
elif a < b:
    print('%d 小于 %d' % (a,b))
else:
    print("未知")
