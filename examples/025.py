#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
求1+2!+3!+...+20!的和
'''

# 求1+2!+3!+...+20!的和。
factorial = 1
sum = 0
for i in range(1, 20 + 1):
    factorial = factorial * i
    sum += factorial
print("1+2!+3!+...+20! =", sum)