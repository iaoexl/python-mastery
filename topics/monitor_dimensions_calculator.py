#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
显示器长宽计算
'''

import math
c = int(input("请输入尺寸（英寸）："))
k = input("请输入比例（16/9）：")
k1 = k.split('/')[0]
k2 = k.split('/')[1]
k = int(k1)/int(k2)
c = c * 2.54
b = math.sqrt(c * c / (k * k + 1))
a = k * math.sqrt(c * c / (k * k + 1))

print("长为：%f（厘米） 宽为：%f（厘米）" % (a, b))