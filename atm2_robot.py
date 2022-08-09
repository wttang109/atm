# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 11:02:23 2020

@author: Sunny
"""
import socket
import json
import atm2_path

msg,RunTime = atm2_path.main()
#RunTime = 1
#msg=[0,1,2]

#print(msg,RunTime)
def sendMsg(m):
    jMsg = json.dumps(m)
    client.sendall(jMsg.encode("utf-8"))
    print("Wait receive data......")
    try:
        receive = client.recv(4000)
#        print(receive)
        jRec = json.loads(receive.decode("utf-8"))
        print("---------------")
        print("Send: " + jMsg[:40] )
        print("")
        print("Receive: " + str(jRec)[:40] ) 
        print("---------------")
    except socket.timeout:
        print('get timeout')
#end = time.time()
#print(end-sst)

try:
    print('try flow')
    for t in range(RunTime):
        for i in range(len(msg)):
            sendMsg(msg[i])
            print('Send msg','###',i, '###')
        
        ## read speed for 6 joint
# =============================================================================
#         sendMsg({"dsID":"HCRemoteMonitor", "cmdType":"query", "queryAddr":["curSpeed-0",
#                                                                            "curSpeed-1",
#                                                                            "curSpeed-2",
#                                                                            "curSpeed-3",
#                                                                            "curSpeed-4",
#                                                                            "curSpeed-5"]})
#         sendMsg({"dsID":"www.hc-system.com.RemoteMonitor", "reqType":"command", "cmdData":["clearAlarmContinue"]})
# =============================================================================
#            time.sleep(2)
#    origin["emptyList"]="0"
#    sendMsg(origin)
    sendMsg({"dsID":"www.hc-system.com.RemoteMonitor", "reqType":"command","cmdData":["startButton"]})
    
except:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = "***"
    Port = 3388
    client.settimeout(10)
    client.connect_ex((IP, Port))
    print("Connect successful......")
    print('except flow')
    for t in range(RunTime):
        for i in range(len(msg)):
            sendMsg(msg[i])
            print('Send msg','###',i, '###')
    sendMsg({"dsID":"www.hc-system.com.RemoteMonitor", "reqType":"command","cmdData":["startButton"]})
    
finally:
#        sendMsg({"dsID":"www.hc-system.com.RemoteMonitor", "reqType":"command","cmdData":["stopButton"]})
#    print('Start Point:',[str(rx),str(ry),str(rz)])
#    print(PathFile[pf])
    print('finished')
