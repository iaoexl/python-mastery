#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
大华产品信息爬虫
'''

import os, re, time, requests
import urllib.request
from bs4 import BeautifulSoup
from urllib import request


def whtml(title, ajax_url):
    print(title, ajax_url)
    wp = request.urlopen(ajax_url)
    content = wp.read()
    if not os.path.exists(now):
        os.mkdir(now)
    name = now + "\\" + title + ".html"
    fp = open(name, "w+b")
    fp.write(content)
    fp.close()


def h2class(url_info, ajax_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    req = urllib.request.Request(url=url_info, headers=headers)
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    all_a = soup.find('div', class_='info-font fr').find_all('h2')
    now2 = '--' + time.strftime("%H%M%S", time.localtime(time.time()))
    for h2 in all_a:
        title = h2.get_text()
        title = re.sub('[/!@#$]', '_', title) + now2
        whtml(title, ajax_url)


def dhinfo(url):
    data = requests.get(url).text
    dhinfo = re.findall(r"https://www.dahuatech.com/product/info/(\d+).html", data)
    dhinfo1 = sorted(set(dhinfo), key=dhinfo.index)
    for url in dhinfo1:
        time.sleep(1)
        url_info = ("https://www.dahuatech.com/product/info/%s.html" % url)
        ajax_url = ("https://www.dahuatech.com/ajax/product/%s/2" % url)
        h2class(url_info, ajax_url)


def product():
    data = requests.get('https://www.dahuatech.com/product.html').text
    product = re.findall(r"https://www.dahuatech.com/product/lists/[1,9]\d*\.html\?area=[1,9]\d*", data)
    product1 = sorted(set(product), key=product.index)
    for url in product1:
        print(url)
        time.sleep(1)
        dhinfo(url)


if __name__ == '__main__':
    now = 'DH' + time.strftime("%Y%m%d", time.localtime(time.time()))
    product()