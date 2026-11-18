#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
某个公司采用公用电话传递数据，数据是四位的整数，在传递过程中是加密的，加密规则如下：每位数字都加上5,然后用和除以10的余数代替该数字，再将第一位和第四位交换，第二位和第三位交换。
'''
if __name__ == '__main__':
    a = str(input('输入一个要加密的四位数字:'))
    L = []
    for i in range(len(a)):
        L.append(a[i])
    for i in range(len(L)):
        L[i] = (int(L[i]) + 5) % 10
    L.reverse()
    print (L)
