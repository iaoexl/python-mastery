#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
输出一个随机数。
'''
import random
x = int(input('请输入随机数起始位置:'))
y = int(input('请输入随机数结束位置:'))
print(random.uniform(x,y))
