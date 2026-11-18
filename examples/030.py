#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
一个5位数，判断它是不是回文数。即12321是回文数，个位与万位相同，十位与千位相同
'''
a = input("输入一串数字: ")
b = a[::-1]
if len(a)!=5 or len(str(a.isdigit()))!= 4:
    print("输入错误")
else:
    if a == b:
        print("%s 是回文"% a)
    else:
        print("%s 不是回文"% a)
