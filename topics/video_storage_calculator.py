#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
3600 一小时有3600秒；0.9 磁盘格式化的损失10%空间；
bit 码流； hour 小时；day 天数；capacity 容量;cc 容量单位；line 图像路数；
bit / 8 * 3600 * hour * day / 0.9 = capacity
'''

print("欢迎使用视频\'存储容量\'和\'存储天数\'计算工具")
while True:
    cla = input("计算存储容量输入1，计算存储天数输入2：\n")
    if cla == '1':
        bit = int(input("请输入码流(kb/s)："))
        hour = int(input("请输入每天录像多少小时(H)："))
        day = int(input("请输入录像天数(d)："))
        line = int(input("请输入图像路数:"))
        capacity = bit / 8 * 3600 * hour * day * line/ 0.9
        cc = int(input("判断所需容量单位【TB输入1;GB输入2;MB输入3;KB输入4】：\n"))
        if cc == 1:
            capacityT = capacity / (1024 * 1024 * 1024)
            print("需要%sTB的硬盘" % capacityT)
        elif cc == 2:
            capacityG = capacity / (1024 * 1024)
            print("需要%sGB的硬盘" % capacityG)
        elif cc == 3:
            capacityM = capacity / 1024
            print("需要%sMB的硬盘" % capacityM)
        elif cc == 4:
            print("需要%sKB的硬盘" % capacity)

    elif cla == '2':
        bit = int(input("请输入码流(kb/s)："))
        hour = int(input("请输入每天录像多少小时(H)："))
        line = int(input("请输入图像路数:"))
        cc = input('请输入容量，例如10T/100G/1000M：')
        if cc[-1] in ['T']:
            capacity = float(cc[0:-1]) * 1024 * 1024 * 1024
        elif cc[-1] in ['G']:
            capacity = float(cc[0:-1]) * 1024 * 1024
        elif cc[-1] in ['M']:
            capacity = float(cc[0:-1]) * 1024
        day = capacity / (bit / 8 * 3600 * hour * line / 0.9)
        print("%s硬盘能存%d天视频" % (cc,day))
    else:
        print('输入错误，请重新输入！')
