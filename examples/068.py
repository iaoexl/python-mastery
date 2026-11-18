#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
有n个整数，使其前面各数顺序向后移m个位置，最后m个数变成最前面的m个数
'''

x = 1
while True:
    n = int(input("请输入第%d个数列位数：\n" % x))
    m = int(input("请输入后移位数：\n"))
    number = []
    for i in range(1,n+1):
        number.append(int(input("请输入第%d位数：\n" % i)))
    number2 = number[n - m:n + 1] + number[0:n - m]
    print("原数列为：%s" % number)
    print("移动完成数列为：%s\n" % number2)
    x += 1
