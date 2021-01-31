#!/usr/bin/env python3

import os, sys
from socket import *


class UdpSocket(object):
    def __init__(self, ctype="server"):
        try:
            self.sock = socket(AF_INET, SOCK_DGRAM)
        except Exception as e:
            print("Something wrong in the creating socket. "+e)

    def Server(self, port):
        self.type = "Server"
        self.sock.bind(('', port))
        while True:
            data, addr = self.sock.recvfrom(1024)
            print('Received from %s:%s.' % addr)
            print('data: ' + data.decode('utf-8'))
            

    def Client(self, ip, port):
        self.type = "Client"
        self.sock.connect((ip, port))
        while True:
            message = input('send message:>> ')
            if message == "exit":
                break
            self.sock.sendto(message.encode('utf-8'), (ip, port))

if __name__ == "__main__":
    udp = UdpSocket()
    udp.Client("114.214.200.41", 9392)

