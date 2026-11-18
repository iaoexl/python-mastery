#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
贴吧按关键词筛选帖子 URL
'''

import urllib.request
import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time


def writeAl(all_nr_print):
    # now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    # now = time.strftime("%Y%m%d%H", time.localtime(time.time()))
    # fname = (kw + "吧_" + kw2 + now + r".txt")
    fname = (kw + "吧_P" + str(beginPage) + "-P" + str(endPage) + "_" + kw2 + r".txt")
    with open(fname, 'a') as f:
        f.write(all_nr_print+"\n")


def all_nr(full_url):
    html = urlopen(full_url)
    bsObj = BeautifulSoup(html, 'html.parser')
    t1 = bsObj.find_all('a')
    for t2 in t1:
        t3 = str(t2.get('href'))
        t31 = str(t2.get('title'))
        if len(t3) == 13:
            if kw2 in t31:
                all_nr_print = t31 + " " + str(kw2_url) + str(t3)
                print(all_nr_print)
                writeAl(all_nr_print)


def tiebaSpider(kw_url, beginPage, endPage):
    for page in range(beginPage, endPage + 1):
        pn = (page - 1) * 50
        full_url = kw_url + "&pn=" + str(pn)
        print("\n%s"% full_url)
        all_nr(full_url)
        # writeAl(full_url)


if __name__ == '__main__':
    kw = input('请输入贴吧名：')
    beginPage = int(input("请输入起始页："))
    endPage = int(input("请输入结束页："))
    kw2 = input('请输入帖子主题的\"关键词\"：')
    kw_url = "http://tieba.baidu.com/f?"
    kw2_url = "http://tieba.baidu.com"
    kw_key = urllib.parse.urlencode({"kw": kw})
    full_url = kw_url + kw_key
    tiebaSpider(full_url, beginPage, endPage)