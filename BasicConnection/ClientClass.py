#!/usr/bin/env python3

import sys, os
import socket
import threading
import struct
import Handler

# 0. command control,
# 1. resume from break-point
# 2. Multithreading
# 3. support Windows.


def reap():
    while True:
        try:
            result = os.waitpid(-1, os.WNOHANG)
            if not result[0]:
                break
        except Exception:
            break


def ConnectSocket(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock
    except Exception as err:
        print("Something wrong to prepare socket: %s".format(err))
        sys.exit(1)


class TcpClientShell(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.command()

    def command(self):
        while True:
            reap()
            cmd = input("Command/MSG:> ")
            if cmd == "send":
                file = input("file path: ")
                # fork a new process to send file.
                try:
                    pid = os.fork()
                except Exception:
                    print("something wrong in the fork().")
                if pid == 0:
                    filesock = Handler.FileSocket(self.host, self.port)
                    filesock.send_file(file)
                else:
                    print("child pid: ", pid, "would send file.")
            elif cmd == "get":
                file = input("file path: ")
            else:
                if 'cmdSocket' not in locals().keys():
                    cmdSocket = ConnectSocket(self.host, self.port)
                    cmdSocket = Handler.CMDMessage(cmdSocket)
                    # print("A new cmd_socket: ", cmdSocket)
                # if cmdSocket is link:
                state = b'\x01'  # STATE_REQUEST
                cmdSocket.msg_send(state, cmd)


    def get_file(self):
        while True:
            print("recv")
            data = self.sock.recv(1024)
            if not data:
                continue
            print("data from server:", data.decode('utf-8'))

    def close(self):
        self.sock.close()


class TcpClient(object):
    def __init__(self, type, host, port):
        self.host = host
        self.port = port
        self.command()

if __name__ == "__main__":
    # server = EpollServer(9190)
    # server.run()
    client = TcpClientCMD("127.0.0.1", 9190)

