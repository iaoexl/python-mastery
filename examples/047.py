#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
两个变量值互换。
'''
a = int(input("请输入a变量的值: "))
b = int(input("请输入b变量的值: "))
a = a + b
b = a - b
a = a - b
print ("a=%s b=%s" % (a, b))
