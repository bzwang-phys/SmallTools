#!/usr/bin/env python3

import os, sys
import socket
import threading


def usage():
    print("""
    SYNOPSIS
        SimpleTcpRelay listenIP listenPort
    DESCRIPTION
        This script is a simple TCP relay. Olny a single connection is allowed.
    """)


class PlaneRelay(object):
    serv = None
    def __init__(self, listenIP, listenPort, outIP=None, outPort=None):
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            serv.bind((listenIP, listenPort))
            serv.listen(5)
        except Exception as err:
            print("Error: Failed to listen on {0}:{1}".format(listenIP,listenPort))
            print("Error Messsage: " + err)
            sys.exit(0)
        print("Listening on {0}:{1}".format(listenIP,listenPort))
        while True:
            clientSock, clientAddr = serv.accept()
            print("[==>]  Incoming connection from {0}".format(clientAddr))
            outLink = threading.Thread(target=self.relayBox, args=(clientSock, outIP, outPort))
            outLink.start()

    def relayBox(self, localSock, ip, port):
        remoteSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remoteSock.connect((ip,port))
        while True:
            localBuff = localSock.recv(4096)
            if len(localBuff):
                print("[==>] From Local Socket: {0} bytes.".format(len(localBuff)))
                remoteSock.send(localBuff)
                print("[==>] Send to remote.")
            remoteBuff = remoteSock.recv(4096)
            if len(remoteBuff):
                print("[<==] Receive from remote Socket: {0} bytes.".format(len(remoteBuff)))
                localSock.send(remoteBuff)
                print("[<==] Send to local.")

        






def main():
    if len(sys.argv) < 3:
        usage()
    listenIP = sys.argv[1]
    listenPort = int(sys.argv[2])

    relay = PlaneRelay(listenIP, listenPort, outIP="202.38.88.230", outPort=9190)


if __name__ == "__main__":
    
    main()

