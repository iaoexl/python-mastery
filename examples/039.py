#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
有一个已经排好序的数组。现输入一个数，要求按原来的规律将它插入数组中。
'''
a = [1,4,7,8]
print("old list:",a)
b = int(input("input num:"))
a.insert(1,b)
a.sort()
print("new list:",a)
