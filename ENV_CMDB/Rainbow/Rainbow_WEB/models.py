#coding:utf-8

from django.db import models

# Create your models here.


class RelatedPerson(models.Model):
    userID = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=11)
    comment = models.TextField(max_length=200)
    department = models.CharField(max_length=30)

    def __st__(self):
        return self.name


class Contract(models.Model):
    num = models.CharField(max_length=30) #合同编号
    name = models.CharField(max_length=30)
    startData = models.DateField()
    endData = models.DateField()
    comment = models.TextField(max_length=500)

    partB = models.CharField(max_length=30) #合同乙方

    def __str__(self):
        return self.name
'''
class RelContractUser(models.Model):
    contract = models.CharField(max_length=30)
    person = models.CharField(max_length=30)

    def __str__(self):
        return self.contract+ " : " + self.person
'''

class RelContractDevice(models.Model):

    contract = models.CharField(max_length=50)
    deviceID = models.CharField(max_length=50)

    def __str__(self):
        return self.contract + " : " +  self.deviceID

class RelPersonDevice(models.Model):
    deviceID = models.CharField(max_length=50)
    relatedPerson = models.CharField(max_length=50)

    def __str__(self):
        return self.deviceID + " : " + self.relatedPerson


class Device(models.Model):
    deviceID = models.CharField(max_length=50)
    masterID = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)
    type = models.BooleanField() #是否是虚拟设备
    mark = models.CharField(max_length=50) #设备的具体型号

    comment = models.TextField(max_length=300)

    def __str__(self):
        return self.name

#IDC 作为设备类主要为了继承设备类的一些信息，并不能算真正的设备
class IDC(Device):
    addr = models.CharField(max_length=50)
    tel = models.CharField(max_length=30) #最好保存电话


class Cabinet(Device):
    pass

class Server(Device):
    pass

class RelDevices(models.Model):
    device = models.CharField(max_length=50)
    partDevice = models.CharField(max_length=50)

    def __str__(self):
        return self.device + " : " + self.partDevice


class Memory(Device):
    cap = models.IntegerField() #容量
    speed = models.IntegerField()
    slot = models.IntegerField()


class CPU(Device):
    speed = models.IntegerField()


class Disk(Device):
    speed = models.IntegerField()
    cap = models.IntegerField() #容量

