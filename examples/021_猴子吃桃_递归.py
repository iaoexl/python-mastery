#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
猴子吃桃问题：猴子第一天摘下若干个桃子，当即吃了一半，还不瘾，又多吃了一个第二天
'''

#方法二
def fun(x):
    if x==10:
        return 1
    else:
        return (fun(x+1)+1)*2
print(fun(1))