#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
利用递归方法求5!
'''

# 利用递归方法求5!
def factorial(n):
    if n == 1:
        fn = 1
    else:
        fn = n * factorial(n-1)
    return fn
print(factorial(5))