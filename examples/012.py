#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
判断n-m之间有多少个素数，并输出所有素数
'''

# 判断n-m之间有多少个素数，并输出所有素数。
k = 0
n = int (input("输入起始数n:"))
m = int (input("输入结束数m:"))

if (n < m) :
    for i in range(n,m):
        for j in range(2,i-1):
            if i%j == 0:
                break
        else:
            print(i,end=(' '))
            k += 1
            if k % 5 == 0:
                print()
    print("共有%d个素数" % k)
else:
    print("输入错误！")