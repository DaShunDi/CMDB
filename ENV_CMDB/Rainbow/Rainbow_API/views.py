#coding: utf-8
from django.shortcuts import render
from Rainbow_WEB.models import *
from Rainbow_API.serializers import *
from Rainbow_WEB.models import  *

from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.status import status
from rest_framework import status

import json

class BaseDetail(APIView):
    baseSerializer = serializers.ModelSerializer()
    baseModel = models.Model
    baseRelModel = models.Model

    baseRelPersonDeviceSerializer = RelPersonDeviceSerializer
    baseRelContractDeviceSerializer = RelContractDeviceSerializer
    baseRelDevicesSerializer = RelDevicesSerializer

    baseRelPersonDeviceModel = RelPersonDevice
    baseRelContractDeviceModel = RelContractDevice
    baseRelDevicesModel = RelDevices

    '''
    baseRelPersonDeviceSerializer = serializers.ModelSerializer
    baseRelContractDeviceSerializer = serializers.ModelSerializer
    baseRelDevicesSerializer = serializers.ModelSerializer
    '''
    def saveOne(self,data):
        print("all saveOne")
        try:
            serializer = self.baseSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return 0
            else:
                return  1
        except Exception as e:
            print(e)
            return 2

    def delOne(self,deviceID):
        try:
            model = self.baseModel.objects.filter(deviceID = deviceID)
            model.delete()
            return 0
        #except  self.baseSerializer.DoesNotExist:
        except  Exception as e:
            print(e)
            return 1

    def delRelAboutDevice(self, deviceID):
        try:
            model  = self.baseRelPersonDeviceModel.objects.filter( deviceID = deviceID)
            model.delete()
            model  = self.baseRelContractDeviceModel.objects.filter( deviceID = deviceID)
            model.delete()
            # 需要把设备关系表重主副内容都删除干净
            model  = self.baseRelDevicesModel.objects.filter( device = deviceID)
            model.delete()
            model  = self.baseRelDevicesModel.objects.filter( partDevice = deviceID)
            model.delete()
            return 0
        except Exception as e:
            print(e)
            return 1

        return 2
    '''
    def delRelPersonDevice(self, relatedPerson="None", deviceID=""):
        try:
            model  = self.baseRelPersonDeviceModel.objects.filter( deviceID = deviceID)
            model.delete()
            return 0
        except Exception as e:
            print(e)
            return 1

        return 2

    def delRelContractDevice(self, deviceID = '0000'):
        try:
            model  = self.baseRelPersonDeviceModel.objects.filter( deviceID = deviceID)
            model.delete()
            return 0
        except Exception as e:
            print(e)
            return 1

        return 2

    def delRelDevices(self,deviceA ="None",deviceB = "None"):

        relDevicesItem = {'device': deviceA, 'partDevice':deviceB }
        serializer = self.baseRelDevicesSerializer(data = relDevicesItem)
        if  serializer.is_valid():
            serializer.save()
            return 0
        else:
            return  1

    '''

    def addRelPersonDevice(self, relatedPerson="None", deviceID=""):

        relPersonItem = {'relatedPerson':relatedPerson, 'deviceID':deviceID}
        print(type(relPersonItem))
        #relPersonItem = json.dumps(relPersonItem)
        print(type(relPersonItem))
        try:
            serializer = self.baseRelPersonDeviceSerializer(data = relPersonItem)
            if serializer.is_valid():
                serializer.save()
                return 0
        except Exception as e:
            print(e)
            return 2

        return 1


    def addRelContractDevice(self,contract='0000', deviceID = '0000'):
        relContractItem = {'contract':contract, 'deviceID':deviceID}

        serializer = self.baseRelContractDeviceSerializer(data = relContractItem)

        if  serializer.is_valid():
            serializer.save()
            return 0
        else:
            return  1

    def addRelDevices(self,deviceA ="None",deviceB = "None"):

        relDevicesItem = {'device': deviceA, 'partDevice':deviceB }
        serializer = self.baseRelDevicesSerializer(data = relDevicesItem)
        if  serializer.is_valid():
            serializer.save()
            return 0
        else:
            return  1

    def post(self,request):
        testData = request.data['add']
        for item in request.data["add"]:
            if self.saveOne(item):
                return Response(item, status = status.HTTP_400_BAD_REQUEST)
            if self.addRelPersonDevice(deviceID = item['deviceID']):
                return Response(item, status = status.HTTP_400_BAD_REQUEST)
            if self.addRelContractDevice(deviceID=item['deviceID']):
                return Response(item, status = status.HTTP_400_BAD_REQUEST)

            if self.addRelDevices(deviceA=item['masterID'], deviceB=item['deviceID']):
                return Response(item, status = status.HTTP_400_BAD_REQUEST)

        return Response(status = status.HTTP_201_CREATED)


    def delete(self,request):
        for item in request.data["del"]:
            print(item)
            if self.delOne(item):
                return Response(status = status.HTTP_404_NOT_FOUND)
            if self.delRelAboutDevice(item):
                return Response(status = status.HTTP_404_NOT_FOUND)

        return Response(status = status.HTTP_200_OK)

'''
class BaseDeviceDetail(BaseDetail):

    baseRelPersonDeviceSerializer = RelPersonDeviceSerializer
    baseRelContractDeviceSerializer = RelContractDeviceSerializer
    baseRelDevicesSerializer = RelDevicesSerializer

    def addRelPersonDevice(self, relatedPerson="", deviceID=""):

        relPersonItem = {'relatedPerson':relatedPerson, 'deviceID':deviceID}

        serializer = self.baseRelPersonDeviceSerializer(data = relPersonItem)
        if  serializer.is_valid():
            serializer.save()
            return 0
        else:
            return  1

    def addRelContractDevice(self,contract='', deviceID = ''):
        if not contract and not deviceID:
            return 2

        relContractItem = {'contract':contract, 'deviceID':deviceID}

        serializer = self.baseRelContractSerializer(data = relContractItem)

        if  serializer.is_valid():
            serializer.save()
            return 0
        else:
            return  1

    def addRelDevices(self,deviceA ="",deviceB = ""):

        if not deviceA and not deviceB:
            return  2

        relDevicesItem = {'aDeviceID': deviceA, 'bDeviceID':deviceB }
        serializer = self.baseRelDevicesSerializer(data = relDevicesItem)
        if  serializer.is_valid():
            serializer.save()
            return 0
        else:
            return  1

    def post(self,request):
        for item in request.data["add"]:
            if self.saveOne(item):
                return Response(item, status = status.HTTP_400_BAD_REQUEST)
            if self.addRelPersonDevice(relatedPerson="",deviceID = item['deviceID']):
                return Response(item, status = status.HTTP_400_BAD_REQUEST)
            if self.addRelContractDevice(contract="", deviceID=item['deviceID']):
                return Response(item, status = status.HTTP_400_BAD_REQUEST)

            if self.addRelDevices(deviceA=item['masterID'], deviceID=item['deviceID']):
                return Response(item, status = status.HTTP_400_BAD_REQUEST)

        return Response(status = status.HTTP_201_CREATED)


    def delete(self,request):
        for item in request.data["del"]:
            print(item)
            if self.delOne(item):
                return Response(status = status.HTTP_404_NOT_FOUND)

        return Response(status = status.HTTP_200_OK)

'''

class ServerDetail(BaseDetail):
    baseSerializer = ServerSerializer
    baseModel = Server



class MemoryDetail(BaseDetail):
    baseSerializer = MemorySerializer
    baseModel = Memory

class DiskDetail(BaseDetail):
    baseSerializer = DiskSerializer
    baseModel =  Disk

class CPUDetail(BaseDetail):
    baseSerializer = CPUSerializer
    baseModel =  CPU
