#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
使用while循环实现输出2-3+4-5+6...+100 的和
'''

i,su = 2,0
while i <= 100:
    if i % 2 == 0:
        su = su + i
    else:
        su = su - i
    i += 1
print(su)
