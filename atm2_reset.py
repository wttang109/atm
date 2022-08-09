# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 11:06:29 2020

@author: Sunny
"""

import socket
import json
import time


def sendMsg(msg):
    try:
        jMsg = json.dumps(msg)
        client.sendall(jMsg.encode("utf-8"))
        print("Wait receive data......")
        receive = client.recv(4000)
        jRec = json.loads(receive.decode("utf-8"))
        print("---------------")
        print("Send: " + jMsg)
        print("")
        print("Receive: " + str(jRec))
        print("---------------")
    finally:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP = "***"
        Port = 3388
        client.settimeout(10)
        client.connect_ex((IP, Port))
        print("Connect successful......")
        jMsg = json.dumps(msg)
        client.sendall(jMsg.encode("utf-8"))
        print("Wait receive data......")
        receive = client.recv(4000)
        jRec = json.loads(receive.decode("utf-8"))
        print("---------------")
        print("Send: " + jMsg)
        print("")
        print("Receive: " + str(jRec))
        print("---------------")


test = {"dsID": "HCRemoteCommand", "emptyList": "1", "dsData": [{"camID": "0", "data": [
    {"oneshot": "1", "action": "4",
     "xpos": "-3.583",
     "ypos": "18.211",
     "zpos": "-24.201",
     "upos": "1.506",
     "vpos": "-123.273",  ##
     "wpos": "-1.427",
     "speed": "10.0", "delay": "0.0", "smooth": "9"}]}]}

reset = {"dsID": "HCRemoteCommand", "emptyList": "1", "dsData": [{"camID": "0", "data": [
    {"oneshot": "1", "action": "4",
     "xpos": "-3.583",
     "ypos": "18.211",
     "zpos": "-24.201",
     "upos": "1.506",
     "vpos": "-83.273",  # -83.273
     "wpos": "-1.427",
     "speed": "10.0", "delay": "0.0", "smooth": "9"}]}]}

startButton = {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["startButton"]}
stopButton = {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["stopButton"]}
actionStop = {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["actionStop"]}
actionPause = {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["actionPause"]}
cAContinue = {"dsID": "HCRemoteMonitor", "cmdType": "command", "cmdData": ["clearAlarmContinue"]}

curAlarm = {"dsID": "HCRemoteMonitor", "reqType": "query", "queryAddr": ["curAlarm"]}
curSpeed = {"dsID": "HCRemoteMonitor", "reqType": "query", "queryAddr": \
    ["curSpeed-0", "curSpeed-1", "curSpeed-2", "curSpeed-3", "curSpeed-4", "curSpeed-5"]}


def Stop():
    sendMsg(stopButton)
    time.sleep(0.1)
    sendMsg(stopButton)


def Reset():
    sendMsg(reset)
    sendMsg(startButton)


def GoTest():
    sendMsg(test)
    sendMsg(startButton)


# sendMsg(curSpeed)
# sendMsg(curAlarm)
def main():
    Stop()
    Reset()


if __name__ == '__main__':
    main()
# =============================================================================
# def main(cmd):
#     if cmd == '1':
#         Stop()
#     elif cmd == '2':
#         GoTest()
#     elif cmd == '3':
#         Reset()
# if __name__=='__main__':
#     while True:
#         cmd = input('cmd: ')
#         main(cmd)
#         if cmd =='q':
#             break
# =============================================================================
