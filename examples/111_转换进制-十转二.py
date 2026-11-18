#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
python操作
'''

import re
def OutPut(num):
    fname = ("demo_out.txt")
    with open(fname, 'a+') as f:
        # f.write(num.encode("gbk", "ignore").decode("gbk") + "\n")
        f.write(num.encode("gbk", "ignore").decode("gbk"))
def my_bin(num4):
    la = []
    if num4 < 0:
        return '-' + my_bin(abs(num4))
    while True:
        num4, remainder = divmod(num4, 2)
        la.append(str(remainder))
        if num4 == 0:
            return ''.join(la[::-1])
if __name__ == '__main__':
    for line in open("demo.txt"):
        num4 = int(re.split("[|]", line)[4])
        num0 = re.split("[|]", line)[0]
        num1 = re.split("[|]", line)[1]
        num2 = re.split("[|]", line)[2]
        num3 = re.split("[|]", line)[3]
        num5 = re.split("[|]", line)[5]
        my_bin(num4)
        num = str(num0) + '|' + str(num1) + '|' + str(num2) + '|' + str(num3) + '|' + str(my_bin(num4)) + '|' + str(num5)
        print(num)
        OutPut(num)