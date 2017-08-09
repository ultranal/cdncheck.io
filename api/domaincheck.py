#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
from multiprocessing import Pool, Lock
from multiprocessing.dummy import Pool as ThreadPool

lock = Lock()
cmpTgt = ""
targetIp = ""

def testIp(url):
    # lock.acquire()
    # print 'http://'+targetIp
    # print url
    # print
    # lock.release()
    host = {'Host': url}
    # s0 = "checking domain %s... " % (url, )
    ret = False
    sFlag = 'undefined'
    try:
        r = requests.get('http://'+targetIp, headers = host, timeout = 5, allow_redirects=False)
        if cmpTgt in r.text:
            s0 = '命中'
            sFlag = 'success'
            ret = True
        else:
            s0 = '响应比对失败'
            sFlag = 'undefined'
            ret = False
    except requests.exceptions.Timeout:
        s0 = '连接超时'
        sFlag = 'warning'
        ret = False
    except requests.exceptions.HTTPError:
        s0 = 'HTTP响应码错误'
        sFlag = 'warning'
        ret = False
    except requests.exceptions.ConnectionError:
        s0 = '连接失败'
        sFlag = 'warning'
        ret = False
    # lock.acquire()
    # print s0
    # lock.release()
    return {'domain':url, 'status': ret, 'statusFlag': sFlag, 'statusinfo': s0}

def domainlookup(url, domainlist, spec, onlySuccFlag):
    pool = ThreadPool(20)
    global targetIp, cmpTgt
    targetIp = url
    fUrl = domainlist
    # print fUrl
    # fUrl = map(str.split, fUrl)
    cmpTgt = spec

    ret = pool.map(testIp, fUrl)
    relret = []
    for x in ret:
        if x['status']:
            relret.append(x)
    for x in ret:
        if not onlySuccFlag and not x['status']:
            relret.append(x)
    return relret
    
            