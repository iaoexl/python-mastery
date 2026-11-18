#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
时间函数举例3。
'''
if __name__ == '__main__':
    import time
    start = time.process_time() # time.perf_counter
    for i in range(10000):
        print (i)
    end = time.process_time()
    print ('different is %6.3f' % (end - start))
