#/usr/bin/python
#-*- coding:utf-8 -*-

import socket

def getLocalIp():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip
