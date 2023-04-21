#!/usr/bin/env python3

import os, sys
import time
import argparse
from time import gmtime, strftime


parser = argparse.ArgumentParser()
parser.add_argument("ethn", help="Specify the network card")
parser.add_argument("-b", "--byte", action="store_true", help="print the results with byte/s.")
parser.add_argument("-a", "--average", action="store_true", help="print the average data in 5s.")
args = parser.parse_args()

ethn = args.ethn
# isByte = args.byte
# isavg = args.average

def ReadData(ethn):
    with open("/proc/net/dev", "r") as f:
        data = ""
        for l in f:
            if not ethn in l:
                continue
            data = l
        if len(data) == 0:
            print("The network card '{0}' can not be found.".format(ethn))
        receive = data.split()[1]
        transmit = data.split()[9]
        return int(receive), int(transmit)

def FormatPrint(data, pre=""):
    if data < 1024:
        formatData = "{1} {0:5.1f} B/s".format(data, pre)
    elif data > 1048576:
        formatData = "{1} {0:5.2f} MB/s".format(data/1048576, pre)
    else:
        formatData = "{1} {0:5.2f} KB/s".format(data/1024, pre)
    return formatData


count = 5
# if isavg:
#     count = 5
receiveList = []
sendList = []
for i in range(count):
    r_start, t_start = ReadData(ethn)
    time.sleep(1)
    r_end, t_end = ReadData(ethn)
    r_delta = r_end - r_start
    t_delta = t_end - t_start
    receiveList.append(r_delta)
    sendList.append(t_delta)

now = strftime("[%m-%d %H:%M:%S]", gmtime())
r_avg = sum(receiveList)/len(receiveList)
t_avg = sum(sendList)/len(sendList)
with open("/home/z/pcap/NetTraffic.log", "a") as f:
    f.write("{0}  average receive:{1}, average send:{2}.\n".format(now, FormatPrint(r_avg), FormatPrint(t_avg)) )

    
if (r_avg > 5*1024*1024 or t_avg > 5*1024*1024):
    now = strftime("%m-%d_%H.%M", gmtime())
    fname = "/home/z/pcap/{0}.pcap".format(now)
    os.system("/usr/sbin/tcpdump -i eth0 -w {0} -c 50000".format(fname))
sys.exit(0)
