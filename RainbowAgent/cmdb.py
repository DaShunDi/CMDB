#coding=utf-8

import pickle
import os

import httplib

def getDigest(inStr):
    '''得到一个字符串的md5值
    如果传入其他类型，返回空'''
    import hashlib
    import types

    m = hashlib.md5(inStr)

    return m.hexdigest()


def writePickle(dD,dI):
    with open('./info.pkl', 'w') as fileInfo:
        pickle.dump(dI, fileInfo)

    with open('./digest.pkl', 'w') as fileDigest:
        pickle.dump(dD, fileDigest)

def getInfo():

    with open('./cmdrst.t' ,'r') as tmp:
        import pickle
        tmpRst =  pickle.load(tmp)
        # print tmpRst
        # try:
        # shell_command = "dmidecode -q -t memory "
        # status,output = commands.getstatusoutput(shell_command)

        # if status != 0:
        #   return setRst



    return tmpRst

def doInfo(tmpInfo):
    mems = tmpInfo.split("Memory Device")

    # 关于内存需要抓取内容
    # 概况信息：　Location,Use,Maximum Capacity,Mumber Of Devices
    # 分信息: Total Width,Data Width,Size,Lactaor,Type,Speed,Manufacturer
    # 　　　　Serial Number,Asset Tag,PartNumbe

    lstMemArray = ['Location', 'Use', 'Maximum Capacity', 'Mumber Of Devices']
    lstMemDevice = ['Total Width', 'Data Width', 'Size', 'Locator', 'Type', 'Manufacturer',
                    'Speed', 'Serial Number', 'Asset Tag', 'Part Number', 'Rank']

    dicRst = dict()

    for memItem in mems:
        item = memItem.strip()
        itemList = item.split("\n\t")
        dicMemDevice = dict()
        for i in itemList:
            l = i.split(':')
            k = l[0]
            if len(l) > 1:
                v = l[1]
            else:
                v = ""

            if k in lstMemArray:
                if 'MemArray' not in dicRst.keys():
                    dicRst['MemArray'] = set()
                dicRst['MemArray'].add((k, v))

            if k in lstMemDevice:
                dicMemDevice[k] = v

        if dicMemDevice and "Serial Number" in dicMemDevice.keys():
            if dicMemDevice['Serial Number'].strip() == 'Not Specified':
                break
            keyTmp = 'MemDevice_' + dicMemDevice['Serial Number'].strip()
            if keyTmp not in dicRst.keys():
                dicRst[keyTmp] = set()
            for k in dicMemDevice.keys():
                dicRst[keyTmp].add((k, dicMemDevice[k]))

    return dicRst


def getPickledInfo():
    '''需要保存本地的内容为：
        1：总信息的MD5及有必要单项信息的md5，存入字典
        2：由单项信息构成的字典数据，嵌套格式
        3:
        具体存储信息格式如下：
        dicDigest:字典形式，存储信息的md5
        dicDigest= { "all": xxxxx, #总信息md5
                     "mem": xxxxx, #内存信息md5
                     "server:xxxx, #server信息md5
                    }

        dicInfo
        '''

    if os.path.exists("./digest.pkl"):
        with open("./digest.pkl", 'r') as fileDigest:
            dicDigest = pickle.load(fileDigest)

    if os.path.exists("./info.pkl"):
        with open("./info.pkl", 'r') as fileInfo:
            dicInfo = pickle.load(fileInfo)

    return dicDigest,dicInfo

def cacInfo(dicKey,newSet,dicInfo):
    '''
    计算最后结果，分两个集合，添加和删除的集合
    :param dicKey:
    :param newSet:
    :return: {"del":{(k1,v1),(k2,v2)...}, "add":{(k1,v1),(k2,v2),...}}
             分别放需要删除的旧值和需要增加的新值， update = del + add
    '''

    # 每次比较都有可能更改持久化内容
    savedDigest,savedInfo = getPickledInfo()

    # 项目增加的时候，需要严格按照先删除后增加的顺序，否则出现逻辑错误
    setRst = {}
    # 计算需要删除的项目
    if dicKey in savedInfo.keys():
        setRst['del'] = savedInfo[dicKey] - newSet
    else:
        setRst['del'] = {}

    # 计算需要增加的项目
    if dicKey in savedInfo.keys():
        setRst['add'] = newSet - savedInfo[dicKey]
    else:
        setRst['add'] = newSet

    # 更新持久化结果
    if dicKey in savedInfo.keys():
        savedInfo[dicKey] = savedInfo[dicKey] - setRst['del'] | setRst['add']
    else:
        savedInfo[dicKey] = setRst['add']

    savedDigest[dicKey] = getDigest(dicInfo[dicKey].__str__())
    # 最后需要更新总信息的digest
    savedDigest['all'] = getDigest(dicInfo.__str__())

    # 写入
    writePickle(savedDigest,savedInfo)

    return setRst


def sendMsg(msg):
    headers = {'Content-type': 'application/json'}


    try:
        conn = httplib.HTTPConnection(
            '127.0.0.1',
            8000,
            100
        )

        '''
        conn.request(
            'POST',
            '/hallo/',
            body = msg.__str__(),
            headers = headers
        )
        '''
        conn.send(msg.__str__())

        rsp = conn.getresponse()
        rst = rsp.read()

        return rst
    except Exception,e:
        print e.message, e.args
        print  "Error by response of memory in BaseGetter.sendMsg"


    return 'error in sendMsg'

'''
allInfo = getInfo()
print("ALLINFO:")
print(allInfo)


dicInfo = doInfo(allInfo)
print("DICINFO:")
print(dicInfo)

savedDigest,savedInfo = getPickledInfo()
print 'savedDigest:'
print savedDigest
print 'savedInfo:'
print savedInfo

rst = dict()
for dickey in dicInfo.keys():
    tmpRst = cacInfo(dickey,dicInfo[dickey],dicInfo)
    rst[dickey] = tmpRst
print "LAST RST:"
print rst
'''

msg = {"Hallo":"Hi,just for testing"}
rst = sendMsg(msg)
print rst

