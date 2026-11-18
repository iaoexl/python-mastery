#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
按相反的顺序输出列表的值。
'''

print("输入格式为\"1234\"")
s = input()
print(type(s),s)
a = list(s)
print(a[-1::-1])
