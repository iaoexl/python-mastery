#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
BMI 健康测算
'''

height = int(input('请输入身高（cm）'))
weight = int(input('请输入体重（kg）'))
BMI = weight/(height*height/10000)
# print(BMI)
if BMI < 18.5:
    print('过轻')
elif 18.5 <= BMI < 24.0:
    print('正常')
elif 24.0 <= BMI < 28.0:
    print('过重')
else:
    print('肥胖')