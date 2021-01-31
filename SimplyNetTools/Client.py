#!/usr/bin/env python3

import os, sys
import socket
import threading


def usage():
    print("""
    A simplest message Client.
    """)


def client(ip, port):
    try:
        localSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        localSock.connect((ip, port))
    except Exception as err:
        print("Error in connection!")
        print(err)
    
    threading.Thread(target=recvMsg, args=(localSock,)).start()
    sendMsg(localSock)

def sendMsg(localSock):
    while True:
        cmd = input("MSG:> ")
        localSock.sendall(bytes(cmd, encoding='utf-8'))

def recvMsg(localSock):
    while True:
        recvData = localSock.recv(1024)
        if len(recvData):
            print("[<==]: " + str(recvData,encoding='utf-8'))


def main():
    # client("202.38.88.230", 9190)
    client("202.38.88.230", 9190)

if __name__ == "__main__":
    main()

