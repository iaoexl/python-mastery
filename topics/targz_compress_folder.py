#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
压缩单个文件
'''
import tarfile
import os

def tar(fname):
    t = tarfile.open(fname + ".tar.gz", "w:gz")
    for root, dir, files in os.walk(fname):
        print (root, dir, files)
        for file in files:
            fullpath = os.path.join(root, file)
            t.add(fullpath)
    t.close()

def untar(fname, dirs):
    t = tarfile.open(fname)
    t.extractall(path = dirs)

if __name__ == "__main__":
    a = input("解压输入\'untar\'；压缩文件夹输入\'tar\'：\n")
    while True:
        if a == 'tar':
            na = input("请输入文件名：\n")
            tar(na)
        elif a == 'untar':
            na = input("请输入文件名：\n")
            untar(na, ".")
        else:
            a = input("解压输入\'untar\'；压缩文件夹输入\'tar\'：\n")
