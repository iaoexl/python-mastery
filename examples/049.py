#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''使用lambda来创建匿名函数。'''
#求圆的面积
area=lambda r:3.1415926*r*r
r=(int(input('请输入半径：')))
print(area(r))
