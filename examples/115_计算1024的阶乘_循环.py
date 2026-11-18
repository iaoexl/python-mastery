#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
循环计算 1024 的阶乘
'''

# 计算1024的阶乘
factorial = 1
for i in range(1, 1024 + 1):
    factorial = factorial * i
print("1024! =", factorial)