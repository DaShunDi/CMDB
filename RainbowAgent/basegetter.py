# coding=utf-8
import pickle
import os
import httplib
import commands

from baseconfig import BaseConfig


class BaseGetter(object):

    dicDigest = dict()
    dicInfo = dict()

    def __inint(self,dataPickleFile, digPickleFile):
        self.dataPickleFile = dataPickleFile
        self.digPickleFile = digPickleFile


    def getDigest(self,inStr):
        '''得到一个字符串的md5值
        如果传入其他类型，返回空'''
        import hashlib
        import types

        if type(inStr) != types.StringType:
            return ""


        m = hashlib.md5(inStr)

        return m.hexdigest()

    def getPickledInfo(self,pickleFile):
        if os.path.exists(pickleFile) :
           with open(pickleFile,'r') as fileInfo:
                dicRst = pickle.load(fileInfo)

        else:
            dicRst = dict()

        return dicRst

    def writePickle(self,data,pickleFile):
        try:
            with open(pickleFile,'w') as fileInfo:
                pickle.dump(data,fileInfo)
        except Exception as e:
            return 1

        return 0

    def makeDiff(self,setOld,setNew):
        '''
        :param setOld:
        :param setNew:
        :return:  dict like {'del':{a,b,c,d},'add':{a,b,c,d}}
        '''
        dicRst = {}

        setTmp = setOld - setNew
        dicRst['del'] = setOld - setNew

        dicRst['add'] = setNew - setOld

        return dicRst

    def sendMsg(self,msg,methode ='POST',url ='/errors/'):
        headers = {'Content-type':'application/json'}

        #FOR TEST


        try:
            conn = httplib.HTTPConnection(
                BaseConfig.HTTP_HOST,
                BaseConfig.HTTP_PORT,
                BaseConfig.HTTP_TIMEOUT
            )

            conn.request(
                methode,
                url,
                body = msg.__str__(),
                headers = headers
            )

            rsp = conn.getresponse()
            rst = rsp.read()
            return rst

        except Exception as e:
            print  "Error by response of memory in BaseGetter.sendMsg"
            print(e)
            return 1

        return  0

    def getServerType(self):
        '''判断此服务器是否是虚拟机'''
        #FOR TEST

        return True
    def getHostname(self):

        #FOR TEST
        hostname = 'TestHost'

        return hostname
    def getUUID(self):
        '''此处可能是虚拟机在使用，为了区分每个个体，使用ＵＵＩＤ作为唯一区分符号
        不知道是否准确，可以更换'''

        rst =""
        ''' 方便调试采用一下代码
        try:
            shell_command = 'dmidecode -q -t system'
            status,rst = commands.getstatusoutput(shell_command)
            if status != 0 :
                return rst
        except:
            return rst
        '''
        if not  os.path.exists('./cmd_system.pkl') :
            try:
                shell_command = 'dmidecode -q -t system'
                status,rst = commands.getstatusoutput(shell_command)

                with open("cmd_system.pkl",'w') as spk:
                    pickle.dump(rst,spk)

            except:
                return rst
        else:
            with open("cmd_system.pkl",'r') as spk:
                rst = pickle.load(spk)

        '''以下代码可能不标准'''
        k  = rst.split('UUID:')
        v = k[1].split('\n\t')

        return v[0]

    # status,output = commands.getstatusoutput(shell_command)

    # if status != 0:
    #   return setRst

    # except:
    #    return setRst




###
### Just for test
###
bg = BaseGetter()
bg.getUUID()

'''
dicDig = {}
dicOld = {"mem":{('o1','one'),('o2',"two"),('o3','three')}}
dicNew = { "mem":{('o1','one'),('n2','zwei'),('o3','drei')} }


bg = BaseGetter()


bg.getPickledInfo()
print "ONE:"
print bg.dicDigest
print bg.dicInfo

rst = bg.getRst('mem',dicOld['mem'])
print "TWO:"
print bg.dicDigest
print bg.dicInfo
print rst

rst = bg.getRst('mem',dicNew['mem'])
print "THREE:"
print bg.dicDigest
print bg.dicInfo
print rst
'''
