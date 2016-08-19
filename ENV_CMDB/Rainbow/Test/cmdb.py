#coding=utf-8

import httplib

def sendMsg(msg):
    headers = {'Content-type': 'application/json'}

    try:
        conn = httplib.HTTPConnection(
            '127.0.0.1',
            8000,
            100
        )

        conn.request(
            'DELETE',
            '/api/cpu/',
            body = msg.__str__(),
            headers = headers
        )
        conn.send(msg.__str__())

        rsp = conn.getresponse()

        rst = rsp.read()

        return rst
    except Exception:
        pass


    return 'error in sendMsg'

#msg = {"Hallo":"Hi,just for testing"}
'''
#j Server testing
msg1 = {
    "add":[{
    "deviceID":"testDevice1",
    "name":"ly",
    "vendor":"tendaTest",
    "type":True,
    "mark":"JUST TEST",
    "comment":"to test the foreignkey"
    }]
}

msg = { "del":["testDevice"]}

'''

'''
#Mem testing
msg1 = {
    "add":[{
        "deviceID":"testMem5",
        "name":"mem5",
        "vendor":"memVendor5",
        "type":True,
        "mark":"JUST TEST for mem",
        "comment":"to test the memory",
        "speed":160,
        "cap":400,
        "slot":5
    }
    ]
}

msg = { "del":["testMem3"]}

'''

'''
#disk
msg1 = {
    "add":[{
        "deviceID":"testDisk1",
        "name":"disk1",
        "vendor":"diskVendor1",
        "type":True,
        "mark":"JUST TEST for mem",
        "comment":"to test the memory",
        "speed":169,
        "cap":407,
    },
        {
        "deviceID":"testDisk2",
        "name":"disk2",
        "vendor":"diskVendor2",
        "type":True,
        "mark":"JUST TEST for mem",
        "comment":"to test the memory",
        "speed":168,
        "cap":40
    }
    ]
}
'''

#disk
msg1 = {
    "add":[{
        "deviceID":"testCPU1",
        "masterID":"server1",
        "name":"cpu1",
        "vendor":"cpuVendor1",
        "type":True,
        "mark":"JUST TEST for mem",
        "comment":"to test the memory",
        "speed":1690,
    },
        {
            "deviceID":"testCPU2",
            "name":"cpu2",
            "masterID":"server2",
            "vendor":"diskVendor2",
            "type":True,
            "mark":"JUST TEST for mem",
            "comment":"to test the memory",
            "speed":16,
        }
    ]
}
msg = { "del":["testCPU1"]}
import json
msg = json.dumps(msg)

rst = sendMsg(msg)
print rst


