#!/usr/bin/env python3

class cls1(object):
    def __init__(self):
        self.a = cls2("Bob")
        print("I'm in cls1's constructor.")

class cls2(object):
    def __init__(self, name):
        print("I'm in cls2's constructor." + name)


ins = cls1()