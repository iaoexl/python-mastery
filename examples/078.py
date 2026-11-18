#! /usr/bin/env python
# -*- coding: utf-8 -*-
# python v3.5+
'''
找到年龄最大的人，并输出。请找出程序中有什么问题。
'''
import operator

person = {
    "li":18,
    "wang":50,
    "zhang":20,
    "sun":22
}
maxname = max(person.items(), key=operator.itemgetter(1))[0]
maxage = max(person.values())
print("年龄最大的是：%s；当下是%s岁" % (maxname,maxage))
