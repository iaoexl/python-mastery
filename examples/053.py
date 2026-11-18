#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
学习使用按位异或 ^
0^0=0; 0^1=1; 1^0=1; 1^1=0
'''
i = int(input("i:"))
j = int(input("j:"))
k = i ^ j
if i == 0 and j == 0 or i == 1 and j == 1 or i == 0 and j == 1or i == 1 and j == 0:
    print('K=%d'% k)
else:
    print('输入错误')
