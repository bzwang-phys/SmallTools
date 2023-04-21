#!/usr/bin/env python3

import sys, os
import socket
from enum import Enum
from BasicConnection import Encrypt


class DecodeMode(Enum):
    Encode = 1
    Decode = 2



class Port(object):
    def __init__(self, ip="0.0.0.0", port=0, mode=DecodeMode.Encode):
        self.ip = ip
        self.port = port
        self.mode = mode


class TcpRelay(object):
    def __init__(self, inIP="", inPort=0, inMode=None, outIP="", outPort=0, outMode=None):
        self.inn = Port(ip=inIP, port=inPort, mode=inMode)
        self.out = Port(ip=outIP, port=outPort, mode=outMode)
        self.encoder = Encrypt.ByteMap()

    def run(self):
        while True:
        self.listenSock

    def listen(self):
        try:
            self.listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listenSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listenSock.bind((self.inn.ip, self.inn.port))
            self.listenSock.listen(5)
        except Exception as err:
            print("Something wrong to prepare socket: %s".format(err))
            sys.exit(1)
    
    def HandleIn(self):



a = TcpRelay("127.0.0.1", 4000)
print(a.inSock)

