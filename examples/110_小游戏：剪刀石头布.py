#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
python操作
'''

import random
while True:
    player = int(input("\n请输入你猜的\"石头-1、剪刀-2、布-3\":\n"))

    computer = int(random.randint(1,3))
    if computer == 1:
        print("电脑出：石头-%d" % computer)
    elif computer == 2:
        print("电脑出：剪刀-%d" % computer)
    else:
        print("电脑出：布-%d" % computer)

    if (player == 1 and computer == 2) or (player == 2 and computer == 3) or (player == 3 and computer == 1):
        print("玩家赢")
    elif computer == player:
        print("平局")
    else:
        print("电脑赢")