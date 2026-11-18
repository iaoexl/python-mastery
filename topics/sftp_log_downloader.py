#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
SFTP 日志定时下载到本地
'''

import paramiko
import os
import time
# 目录和文件名含中文直接爆炸...

def DownLoadFile(sftp, LocalFile, RemoteFile):  # 下载当个文件
    sftp.get(RemoteFile, LocalFile) # 下载目录中文件
    return True


def DownLoadFileTree(sftp, LocalDir, RemoteDir):  # 下载整个目录下的文件

    if not os.path.exists(LocalDir):
        os.makedirs(LocalDir)
    for file in sftp.listdir(RemoteDir):
        Local = os.path.join(LocalDir, file)
        Remote = os.path.join(RemoteDir, file)
        if file.find(".") == -1:  # 判断是否是文件
            if not os.path.exists(Local):
                os.makedirs(Local)
            DownLoadFileTree(sftp, Local, Remote)
        else:  # 文件
            DownLoadFile(sftp, Local, Remote)
    return "complete"


def sftpFoder(sftp):
    ssh = serverConnect()
    stdin, stdout, stderr = ssh.exec_command('ls /home')
    res_list = stdout.readlines()[-1].decode("utf-8", "ignore")

    # 本地文件local/远程目录remote
    local = os.path.join('..', '02', 'OutPut', Ymd, res_list.strip()) + os.sep # Windows文件夹
    remote = '/home/%s/' % res_list.strip()
    # 下载
    DownLoadFileTree(sftp, local, remote)


def serverConnect():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='10.1.22.31', port=22, username='root', password='huanu')
    return ssh


def LoginOS():
    # 登录系统
    transport = paramiko.Transport(('10.1.22.31', 22))
    transport.connect(username='root', password='huanu')
    # 链接sftp
    sftp = paramiko.SFTPClient.from_transport(transport)
    # 去下载筛选
    sftpFoder(sftp)


if __name__ == '__main__':
    # 获取时间/年月日时分秒
    YmdHMS = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    # 获取时间/年月日
    Ymd = time.strftime("%Y%m%d", time.localtime(time.time()))

    # 去登录系统
    LoginOS()