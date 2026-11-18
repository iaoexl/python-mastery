#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
压缩指定文件
'''

import tarfile
import os

def tar(fname):
    with tarfile.open('test.tar.gz', 'w:gz') as tar:
        # tar.add('log.log', arcname ='log.log')
        tar.add(fname, arcname = fname)

if __name__ == "__main__":
    tar('test.py')