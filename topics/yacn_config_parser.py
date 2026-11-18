#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
亚晨 config XML 数据提取
'''

from xml.dom.minidom import parse
import xml.dom.minidom
import time


def AlarmPoint(wAlarmPoint):
    fname = (now + "AlarmPoint.txt")
    with open(fname, 'a+') as f:
        f.write(wAlarmPoint.encode("gbk", "ignore").decode("gbk") + "\n")


def AlarmOutput(wAlarmOutput):
    fname = (now + "AlarmOutput.txt")
    with open(fname, 'a+') as f:
        f.write(wAlarmOutput.encode("gbk", "ignore").decode("gbk") + "\n")


def MonitoringPoints(wMonitoringPoints):
    fname = (now + "MonitoringPoints.txt")
    with open(fname, 'a+') as f:
        f.write(wMonitoringPoints.encode("gbk", "ignore").decode("gbk") + "\n")


def ReviceInfo(wReviceInfo):
    fname = (now + "DeviceInfo.txt")
    with open(fname, 'a+') as f:
        f.write(wReviceInfo.encode("gbk", "ignore").decode("gbk") + "\n")


def rAlarmPoint(collection):
    for i in range(1, 9999):
        data = collection.getElementsByTagName("point_%d" % i)
        for root in data:
            try:
                if not root.getElementsByTagName('channel_no'): continue
                org = root.getElementsByTagName('org')[0]
                org = org.childNodes[0].data
                point_name = root.getElementsByTagName('point_name')[0]
                point_name = point_name.childNodes[0].data
                # data2 = collection.getElementsByTagName("channel_0")
                device_id = root.getElementsByTagName('device_id')[0]
                device_id = device_id.childNodes[0].data
                channel_no = root.getElementsByTagName('channel_no')[0]
                channel_no = channel_no.childNodes[0].data
                wAlarmPoint = org + '|' + point_name + '|' + device_id + '|' + channel_no
                print(wAlarmPoint)
                AlarmPoint(wAlarmPoint)
            except IndexError:
                pass
    return GoTo(5)


def rAlarmOutput(collection):
    for i in range(1, 9999):
        data = collection.getElementsByTagName("point_%d" % i)
        for root in data:
            try:
                if not root.getElementsByTagName('dc_1'): continue
                org = root.getElementsByTagName('org')[0]
                org = org.childNodes[0].data
                point_name = root.getElementsByTagName('point_name')[0]
                point_name = point_name.childNodes[0].data
                device_id = root.getElementsByTagName('dc_1')[0].getAttribute('device_id')
                deviceid_name = root.getElementsByTagName('dc_1')[0].getAttribute('deviceid_name')
                channel_id = root.getElementsByTagName('dc_1')[0].getAttribute('channel_id')
                channelid_name = root.getElementsByTagName('dc_1')[0].getAttribute('channelid_name')
                wAlarmOutput = org + '|' + point_name + '|' + device_id + '|' + deviceid_name + '|' + channel_id + '|' + channelid_name
                print(wAlarmOutput)
                AlarmOutput(wAlarmOutput)
            except IndexError:
                pass
    return GoTo(4)


def rMonitoringPoints(collection):
    for i in range(1, 9999):
        data = collection.getElementsByTagName("point_%d" % i)
        for root in data:
            try:
                if not root.getElementsByTagName('ptz_preno'): continue
                org = root.getElementsByTagName('org')[0]
                org = org.childNodes[0].data
                point_name = root.getElementsByTagName('point_name')[0]
                point_name = point_name.childNodes[0].data
                deviceid = root.getElementsByTagName('deviceid')[0]
                deviceid = deviceid.childNodes[0].data
                deviceidname = root.getElementsByTagName('deviceid')[0].getAttribute('name')
                channelid = root.getElementsByTagName('channelid')[0]
                channelid = channelid.childNodes[0].data
                channelidname = root.getElementsByTagName('channelid')[0].getAttribute('name')
                wMonitoringPoints = org + '|' + point_name + '|' + deviceid + '|' + deviceidname + '|' + channelid + '|' + channelidname
                print(wMonitoringPoints)
                MonitoringPoints(wMonitoringPoints)
            except IndexError:
                pass
    return GoTo(3)


def rDeviceInfo(collection):
    for i in range(1, 9999):
        data = collection.getElementsByTagName("device_%d" % i)
        for root in data:
            try:
                if not root.getElementsByTagName('friend_code') or not root.getElementsByTagName('ip_address') or not root.getElementsByTagName('user_name'): continue
                friend_code = root.getElementsByTagName('friend_code')[0]  # 设备编号
                friend_code = friend_code.childNodes[0].data
                device_name = root.getElementsByTagName('device_name')[0]  # 设备名称
                device_name = device_name.childNodes[0].data
                ip_address = root.getElementsByTagName('ip_address')[0]  # 设备IP地址
                ip_address = ip_address.childNodes[0].data
                user_name = root.getElementsByTagName('user_name')[0]  # 设备用户名
                user_name = user_name.childNodes[0].data
                password = root.getElementsByTagName('password')[0]  # 设备密码
                password = password.childNodes[0].data
                server_port = root.getElementsByTagName('server_port')[0]  # 设备端口
                server_port = server_port.childNodes[0].data
                wReviceInfo = friend_code + '|' + device_name + '|' + ip_address + '|' + user_name + '|' + password + '|' + server_port
                print(wReviceInfo)
                ReviceInfo(wReviceInfo)
            except IndexError:
                pass
    return GoTo(2)


def GoTo(i):
    if i == 1:
        DomDeviceInfo = xml.dom.minidom.parse("Config/DeviceInfo.xml")
        collection = DomDeviceInfo.documentElement
        rDeviceInfo(collection)#设备表
    elif i == 2:
        DomDeviceInfo = xml.dom.minidom.parse("Config/Point.xml")
        collection = DomDeviceInfo.documentElement
        rMonitoringPoints(collection)#监控点
    elif i == 3:
        DomDeviceInfo = xml.dom.minidom.parse("Config/Point.xml")
        collection = DomDeviceInfo.documentElement
        rAlarmOutput(collection)#报警输出
    elif i == 4:
        DomDeviceInfo = xml.dom.minidom.parse("Config/Point.xml")
        collection = DomDeviceInfo.documentElement
        rAlarmPoint(collection)#报警点
    else:
        exit()


if __name__ == '__main__':
    now = time.strftime("%Y%m%d", time.localtime(time.time()))
    GoTo(1)