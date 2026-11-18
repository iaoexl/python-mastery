#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
字符串日期转换为易读的日期格式。
'''
from dateutil import parser
dt = parser.parse("Aug 28 2018 09:00PM")
print (dt)
