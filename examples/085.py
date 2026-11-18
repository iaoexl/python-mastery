#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
输入一个奇数，然后判断最少几个 9 除于该数的结果为整数。
程序分析：999999 / 13 = 76923。
'''
def monkey():
    a=int(input('请输入一个\'个位数\'不是5的奇数:\n'))
    b=9
    i=1
    while True:
        if  a % 5 == 0 or a % 2 == 0: # 避免进入死循环
            a = int(input('请输入一个\'个位数\'不是5的奇数:\n'))
        elif b > a and b % a == 0:
            r = b / a
            print('需要{}个9'.format(i))
            print('%d / %d = %d'% (b,a,r))
            break
        else:
            b = b*10+9
            i += 1
if __name__ == '__main__':
    monkey()
