#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
时间函数举例2。
'''
def test():
    for i in range(3000):
        print(i)


if __name__ == '__main__':
    from timeit import timeit
    t = timeit('test()', 'from __main__ import test', number = 1)
    print(t)
