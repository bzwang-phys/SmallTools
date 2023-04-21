#!/usr/bin/env python3

import sys, os, time
import logging
import socket
import select
import threading
from collections import defaultdict
import Handler


TYPE_CMDMSG = b'\x01'
TYPE_FILE = b'\x02'
TYPE_STREAM = b'\x03'
STATE_REQUEST = b'\x01'
STATE_RESPONSE = b'\x02'
ITYPE_CMDMSG = 0x01
ITYPE_FILE = 0x02
ITYPE_STREAM = 0x03
ISTATE_REQUEST = 0x01
ISTATE_RESPONSE = 0x02


POLLNULL = 0b00000000
POLLIN = 0b00000001
POLLOUT = 0b00000010
POLLERR = 0b00000100
POLLHUP = 0b00001000
POLLNVAL = 0b00010000

TIMEOUT = 10




class SelectServer(object):
    def __init__(self, port, ip=''):
        self.sock = ListenSocket(port, ip)
        self.sockfd = self.sock.fileno()
        self.rSet = set(self.sockfd)
        self.wSet = set()
        self.xSet = set()
    
    # This function is used to obtain all events.
    def poll(self, timeout=None):
        r, w, x = select.select(rSet, wSet, xSet, timeout)
        events = defaultdict(lambda: POLLNULL)
        for fd in r:
            events[fd] |= POLLIN
        for fd in w:
            events[fd] |= POLLOUT
        for fd in x:
            events[fd] |= POLLERR
        return events
    
    def register(self, fd, mode):
        if mode & POLLIN:
            rSet.add(fd)
        if mode & POLLOUT:
            wSet.add(fd)
        if mode & POLLERR:
            xSet.add(fd)
    
    def remove(self, fd, mode):
        if (mode & POLLIN) and (fd in self.rSet):
            self.rSet.remove(fd)
        if (mode & POLLOUT) and (fd in self.wSet):
            self.wSet.remove(fd)
        if (mode & POLLERR) and (fd in self.xSet):
            self.xSet.remove(fd)


class KqueueServer():
    pass


class EpollServer(object):
    def __init__(self, port, ip=''):
        self.sock = ListenSocket(port, ip)
        self.sockfd = self.sock.fileno()
        print("socket {0} is ready.".format(self.sockfd))
        self.epoll = select.epoll()
        self.epoll.register(self.sockfd, select.EPOLLIN)

    # This function is used to obtain all events.
    def poll(self, timeout=4):
        events = self.epoll.poll(timeout)
        return events
    
    def register(self, fd, mode):
        self.epoll.register(fd, mode)
    
    def unregister(self, fd, mode=None):
        self.epoll.unregister(fd)
    
    def modify(self, fd, mode):
        self.epoll.modify(fd, mode)




    def write_sock(self, fd):
        while len(self.responses.setdefault(fd, '')):
            length = self.connections[fd].send(self.responses[fd])
            self.responses[fd] = self.responses[fd][length:]

    def read_sock(self, fd):
        self.requests[fd] = self.connections[fd].recv(1024)
        with open("1.png", "ba+") as f:
            f.write(self.requests[fd])
        # print("data received: ", requests[fd])
        # if client closed, we still get a EPOLLIN and return "".
        if not self.requests[fd]:
            self.connections[fd].close()
            del self.connections[fd]
            del self.requests[fd]
            self.epoll.unregister(fd)



class MultiProcServer(object):
    def __init__(self, port):
        self.port = port


def ListenSocket(port, ip=''):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((ip, port))
        sock.listen(5)
    except Exception as err:
        print("Something wrong to prepare socket: %s".format(err))
        sys.exit(1)
    return sock


class ThreadServer(object):
    def __init__(self, port, ip4=''):
        self.sock = ListenSocket(port, ip=ip4)

    def run(self):
        connections = {}
        requests = {}
        responses = {}
        while True:
            try:
                client_sock, client_addr = self.sock.accept()
            except Exception:
                print("something wrong in the sock.accept().")


class SocketHandler(object):
    def __init__(self):
        self.noDataN = 0
        self.typeH = None
        self.handler = None


class Server(object):
    def __init__(self, port, ip=''):
        if hasattr(select, 'epoll'):
            self.server = EpollServer(port, ip)
        elif hasattr(select, 'select'):
            self.server = SelectServer(port, ip)
        elif hasattr(select, 'kqueue'):
            self.server = KqueueServer()
        else:
            raise Exception('can not find any available module in "select" ')
        self.fdDict = {}   #  fd:(sock, sockHandler)
        self.stop = False
    
    def run(self):
        while not self.stop:
            try:
                events = self.server.poll(TIMEOUT)
            except Exception as e:
                logging.info(e)
            # print(events)
            for fd, event in events:
                if fd == self.server.sockfd:
                    clientSock, clientAddr = self.server.sock.accept()
                    clientSock.setblocking(0)
                    clientfd = clientSock.fileno()
                    self.fdDict[clientfd] = (clientSock, SocketHandler())
                    self.server.register(clientfd, POLLIN)
                    logging.info("A connection from %s".format(clientAddr))
                elif event & POLLHUP:
                    self.clear(fd)
                elif event & POLLIN:
                    clientSock, sockHandler = self.fdDict.get(fd, None)
                    if clientSock:
                        data = clientSock.recv(1)
                        if data:
                            self.choose_handler(fd, data)
                            sockHandler.handler.in_event(event, data)
                            self.server.modify(fd, POLLIN | POLLOUT | POLLHUP)
                        if not data:
                            sockHandler.noDataN += 1
                            if sockHandler.noDataN > 6:
                                self.clear(fd)
                    else:
                        logging.warning("Something wrong in clientSock.")
                elif event & POLLOUT:
                    pass

    def clear(self, fd):
        self.server.unregister(fd)
        sock = self.fdDict.get(fd, None)[0]
        sock.close()
        del self.fdDict[fd]
    
    def choose_handler(self, fd, typeH):
        clientSock, sockHandler = self.fdDict.get(fd, None)
        if sockHandler.handler and sockHandler.typeH == typeH:
            return
        if typeH ==  TYPE_CMDMSG: # command/msg
            sockHandler.handler = Handler.CMDMessage(clientSock)
            sockHandler.typeH = TYPE_CMDMSG
        elif typeH ==  TYPE_FILE: # 
            pass


