#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
在文件夹中创建10个文本，以数字给他们命名
'''

import os

def text_creation():
    path = 'd://a//'
    for name in range (1,11):
        with open(path + str(name) + '.txt','w') as text: #写文件
            text.write(str(name))
            text.close()
            print ('创建'+ str(name) + '.txt成功')
text_creation()