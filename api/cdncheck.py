#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
from multiprocessing import Pool, Lock
from multiprocessing.dummy import Pool as ThreadPool

lock = Lock()
tgthead = ""
host = ""
url = ""

def ipify(numIp):
    return "%d.%d.%d.%d" % ((numIp & 0xFF000000) >> 24, (numIp&0xFF0000) >> 16, (numIp&0xFF00) >> 8, numIp&0xFF)

def cidrParser(iprange):
    p = iprange.strip().split('/')
    if len(p) == 1:
        ipaddr = p[0]
        netmask = 32
    else:
        ipaddr = p[0]
        netmask = int(p[1])
    revmask = 32 - netmask
    p = ipaddr.strip().split('.')
    p = map(int, p)
    numIp = p[0]*(1<<24) + p[1]*(1<<16) + p[2]*(1<<8) + p[3]
    netId = numIp >> revmask << revmask
    iplist = []
    for hostId in range((1 << revmask)):
        iplist.append(ipify(netId+hostId))
    return iplist
        
def tryip(tgt):
    h = {'Host':host}
    s0 = ""
    ret = False
    statusFlag = "undefined"
    try:
        r = requests.get(url%(tgt,), headers = h, timeout = 5, allow_redirects=False)

        if tgthead in r.text:
            s0 = '命中'
            statusFlag = 'success'
            ret = True
        else:
            s0 = '比对未命中'
            statusFlag = "undefined"
            ret = False
    except requests.exceptions.Timeout:
        s0 = '连接超时'
        statusFlag = "warning"
        ret = False
    except requests.exceptions.HTTPError:
        s0 = 'HTTP错误'
        statusFlag = "warning"
        ret = False
    except requests.exceptions.ConnectionError:
        s0 = '连接失败'
        statusFlag = "warning"
        ret = False
    return {
        'ip': tgt,
        'status': ret,
        'statusFlag': statusFlag,
        'statusinfo': s0
    }

def iplookup(hostname, iprange, spec, onlySuccFlag):
    global url, host, tgthead
    pool = ThreadPool(20)
    tgtIpRange = iprange
    p = hostname
    if p[:5] == 'https':
        url = 'https://%s' + p[8+p[8:].find('/')]
        host = p[8:8+p[8:].find('/')]
    else:
        url = 'http://%s' + p[7+p[7:].find('/')]
        host = p[7:7+p[7:].find('/')]
    tgthead = spec
    
    success = False
    iplist = cidrParser(tgtIpRange)
    ret = map(tryip, iplist)

    # re-syntax
    relret = []
    for x in ret:
        if x['status']:
            relret.append(x)
    for x in ret:
        if not onlySuccFlag and not x['status']:
            relret.append(x)
    return relret
    # for ip in cidrParser(tgtIpRange):
        # if tryip(ip):
            # print 'IP %s success!' % (ip, )
            # success = True
            # break
    # if not success:
        # print 'All checking failed!'
