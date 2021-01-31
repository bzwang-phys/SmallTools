#!/usr/bin/env python3

import os, sys
import socket
import threading


def usage():
    print("""
    A simplest message Server.
    """)


def server(port, ip=''):
    try:
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv.bind((ip, port))
        serv.listen(5)
    except Exception as err:
        print("Error in connection!")
        print(err)
    while True:
        client, addr = serv.accept()
        print("[<==] Connection from : " + str(addr))
        handle(client)

def handle(sock):
    threading.Thread(target=recvMsg, args=(sock,)).start()
    threading.Thread(target=sendMsg, args=(sock,)).start()

def sendMsg(client):
    while True:
        cmd = input("MSG:> ")
        client.sendall(bytes(cmd, encoding='utf-8'))

def recvMsg(client):
    while True:
        recvData = client.recv(1024)
        if len(recvData):
            print("[<==]: " + str(recvData,encoding='utf-8'))

def main():
    server(9190)


if __name__ == "__main__":
    main()

