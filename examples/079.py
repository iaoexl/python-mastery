#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
字符串排序。
'''
if __name__ == '__main__':
    list1 = []
    for i in range(3):
        str1 = input('请输入第%d个字符串:\n' % (i+1))
        list1.append([str1])
    list1.sort()
    for item in list1:
        print(item,end=' ')
