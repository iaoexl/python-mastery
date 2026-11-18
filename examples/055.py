#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
学习使用按位取反~
~0=1; ~1=0;
'''
if __name__ == '__main__':
    a = int(input("input a:"))
    b = ~a
    print ('The a\'s 1 complement is %d' % b)
    a = ~a
    print ('The a\'s 2 complement is %d' % a)
