#!/usr/bin/env python3

import os

sysCmdList = ['ls']
cmdList = ['sysinfo']

def cmd_exe(cmd):
    if (cmd not in sysCmdList) and (cmd not in cmdList):
        return "command can not be executed."
    if cmd in sysCmdList:
        res = os.system(cmd)
        return res
    if cmd in cmdList:
        pass


