#coding=utf-8
import os
import commands
import httplib

from baseconfig import BaseConfig
import json



from basegetter import BaseGetter
from baseconfig import BaseConfig


class MemGetter(BaseGetter):

    '''有一个Ｂｕｇ，如果硬件整体删除，不能判断，
    需要每次检测总键值,暂时问题不大，以后在慢慢修改'''

    def getDevice(self):
        dicRst = dict()

        try:
            '''
            #FOR TESTING
            shell_command = "dmidecode -q -t memory "
            #shell_command = "ls"
            status,memInfo = commands.getstatusoutput(shell_command)
            '''

            ###start test
            status = 0
            import pickle
            with open('tmp.pkl','r') as tmp:
                memInfo = pickle.load(tmp)
                print(memInfo)
                print
            ###end
            if status != 0:
                return status
        except Exception as e:
            print(e)
            return 2

        mems = memInfo.split("Memory Device")


        #关于内存需要抓取内容
        #概况信息：　Location,Use,Maximum Capacity,Mumber Of Devices
        #分信息: Total Width,Data Width,Size,Lactaor,Type,Speed,Manufacturer
        #　　　　Serial Number,Asset Tag,PartNumbe

        #lstMemArray = ['Location','Use','Maximum Capacity','Mumber Of Devices']
        lstMemDevice = ['Serial Number','Manufacturer','Part Number','Size',\
                        'Speed','Locator','type']

        for memItem in mems:
            item = memItem.strip()
            itemList = item.split("\n\t")
            dicMemDevice = dict()
            for i in itemList:
                l = i.split(':')
                k = l[0]
                if  len(l) > 1:
                    v = l[1]
                else:
                    v = ""

                if k in lstMemDevice:
                    dicMemDevice[k] = v

            if dicMemDevice and "Serial Number" in dicMemDevice.keys() :
                if dicMemDevice['Serial Number'].strip() == 'Not Specified':
                    break
                keyTmp = 'MemDevice_' + dicMemDevice['Serial Number'].strip()
                if keyTmp not in dicRst.keys():
                    dicRst[keyTmp] = dict()
                for k in dicMemDevice.keys():
                    dicRst[keyTmp][k] = dicMemDevice[k].strip()

                for k in dicRst[keyTmp].keys():
                    if k in ['Size','Speed']:
                        v = dicRst[keyTmp][k]
                        dicRst[keyTmp][k] = int( v.strip().split()[0])


                 #整理成对应的API可识别的信息
                dicAPIKey = {'Serial Number':'deviceID','Manufacturer':'vendor','Part Number':'mark',\
                      'Size':'cap','Speed':'speed','Locator':'slot'}
                for i in dicRst[keyTmp].keys():
                    if i in dicAPIKey.keys():
                        dicRst[keyTmp][ dicAPIKey[i]] = dicRst[keyTmp][i]
                        del( dicRst[keyTmp][i])
                dicRst[keyTmp]['masterID'] = self.getUUID()
                dicRst[keyTmp]['comment'] = 'None'
                dicRst[keyTmp]['type'] = self.getServerType()
                dicRst[keyTmp]['name'] = 'memory_device'
                dicRst[keyTmp]['slot'] = 1 
        return dicRst


    def execute(self,kw):
        dicRst = self.getDevice()
        print 'dicRst'
        print dicRst

        #保存就的deviceID作为比对依据
        dicDevice = self.getPickledInfo(BaseConfig.PICKEL_INFO_FILE)
        print "dicDevice"
        print dicDevice

        setDeviceID = set()
        if kw in dicDevice.keys():
            setDeviceID = dicDevice[kw]
        dicKey = self.makeDiff(setDeviceID,set(dicRst.keys()))
        print 'dicKey'
        print dicKey


        if len(dicKey['del']) !=0:
            if self.sendMsg(dicKey['del'],'DELETE',BaseConfig.MEM_URL) != 0:
                return 1

        addInfo = dict()
        addInfo['add'] = list()
        for k in dicKey['add']:
            addInfo['add'].append( dicRst[k] )

        print 'addINFO'
        print addInfo

        addInfo = json.dumps(addInfo)

        print 'addINFO'
        print addInfo

        if len(addInfo) > 0:
            if self.sendMsg(addInfo,'POST',BaseConfig.MEM_URL) != 0:
                return 2







mg = MemGetter()
mg.execute('memory')

