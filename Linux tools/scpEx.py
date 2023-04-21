#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser(description="scpEx")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-df", "--destinationfrom", choices=['fangsh','einstein','computer100','liuserver','zpi'])
group.add_argument("-dt", "--destinationto", choices=['fangsh','einstein','computer100','liuserver','zpi'])
parser.add_argument("-f", "--fromfile")
parser.add_argument("-t", "--tofile")
args = parser.parse_args()

fromfile = args.fromfile
tofile = args.tofile
destination = args.destinationfrom if args.destinationto==None else args.destinationto
fromMachine = args.destinationfrom if args.destinationfrom is not None else "localhost"
toMachine = args.destinationto if args.destinationto is not None else "localhost"


if (args.fromfile is None) and (args.tofile is None):
    print("Error: You need to specify a file to tranfer.")
    exit
if args.fromfile is None:
    fromfile = "~/"
if args.tofile is None:
    tofile = "~/"


serverDict = {
    "fangsh" : "bzwang@114.214.201.115",
    "einstein" : "wangbz@210.45.78.184",
    "computer100" : "wangbz@210.45.72.91",
    "liuserver" : "baozong@162.105.151.155",
    "zpi" : "pi@192.168.1.107",
    "localhost" : ""
}

def connector(server):
    return "" if server=="localhost" else ":"

paraDict = {
    "fangsh" : "-P 123",
    "einstein" : " ",
    "computer100" : " ",
    "liuserver" : " ",
    "zpi" : " "
}

para = paraDict[destination]
fromMachine = serverDict[fromMachine] + connector(fromMachine)
toMachine = serverDict[toMachine] + connector(toMachine)

command = "scp  {0}  {1}{2}  {3}{4}".format(para, fromMachine, fromfile, toMachine, tofile)

print(command)
os.system(command)


