#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字。例如2+22+222+2222+22222(此时共有5个数相加)，几个数相加由键盘控制。
'''

n = int(input('请输入层数：'))
a = int(input('请输入计算数：'))
Su = 0
Tu = []
for i in range(n):
    Tu.append(int(str(a)*(i+1)))
print('创建的数列为：%s' % Tu)

for i in Tu:
    Su = Su + i
print('数列的和为：%s' % Su)
