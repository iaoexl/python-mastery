#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
百钱买百鸡，鸡翁cocks 5钱、鸡母hens 3钱、鸡雏chicks 1/3钱
'''


money = 100
score = 0
for cocks in range(1,21):
    for hens in range(1,34):
        for chicks in range(1,301):
            score = cocks*5 + hens*3 + float(chicks)/3
            if score == money and cocks+hens+chicks == 100:
                print('公鸡%s只,母鸡%s只,小鸡%s只' % (cocks,hens,chicks))
            else:
                pass
