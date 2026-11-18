#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
有两个磁盘文件A和B,各存放一行字母,要求把这两个文件中的信息合并(按字母顺序排列), 输出到一个新文件C中。
'''
def read(filename):
    f = open(filename,"r+")
    a = f.readlines()
    return a
s = list("".join(read("test1.txt")+read("test2.txt")))
s.sort()
s1 = "".join(s)
t = open("test.txt","w+")
t.writelines(s1)
t.close()
