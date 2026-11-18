#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
列表排序及连接。
'''
if __name__ == '__main__':
    a = [1,3,2]
    b = [3,4,5]
    a.sort()     #对列表 a 进行排序
    print(a)
    a.extend(b) #链接列表a与b
    print(a)
