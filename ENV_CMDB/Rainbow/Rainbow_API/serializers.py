from rest_framework import serializers
from Rainbow_WEB.models import *



class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('deviceID','name','vendor','type','mark', \
                  'comment','masterID')


class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Memory
        fields = ('deviceID','name','vendor','type','mark', \
                  'comment', 'masterID','cap','speed','slot')

class DiskSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Disk
        fields = ('deviceID','name','vendor','type','mark', \
                  'comment','masterID', 'cap','speed')

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model =  CPU
        fields = ('deviceID','name','vendor','type','mark', \
                  'comment', 'speed','masterID')

class RelPersonDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model =  RelPersonDevice
        fields = ('deviceID','relatedPerson')

class RelContractDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model =  RelContractDevice
        fields = ('deviceID','contract')
class RelDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model =  RelDevices
        fields = ('device','partDevice')
