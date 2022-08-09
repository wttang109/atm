# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 10:18:32 2020

@author: Sunny
"""
import numpy as np
import vg
import time

# =============================================================================
# #  outside parameters (usb)
# SprayAngle = 30
# RunTime = 1
# SpaceNum = 10
# speed = "80.0"
# rx, ry, rz = 361.965, -7.47, 308.711
# ou, ov, ow = 178.8, 0.7, 177.184    
# xfix, yfix, zfix = 150, -30, 400    
# 
# #  debug parameters
# pf = 11
# RunRobot = 1
# oneshot = "1"
# PicPlot = 0
# Draw_3D = 0
# SinglePic = 0
# =============================================================================
def main(pcPath, pcOthers, agData):
    #  outside parameters (usb)
    f = open('atm2_par.txt', 'r')   ###
    data = f.readlines()
    SprayAngle = int(data[1].split('=')[1])
    RunTime = int(data[2].split('=')[1])
    SpaceNum = int(data[3].split('=')[1])
    speed = data[4].split('=')[1][:-1]
    rx, ry, rz = float(data[5].split('=')[1].split(',')[0]),\
                 float(data[5].split('=')[1].split(',')[1]),\
                 float(data[5].split('=')[1].split(',')[2])
    ou, ov, ow = float(data[6].split('=')[1].split(',')[0]),\
                 float(data[6].split('=')[1].split(',')[1]),\
                 float(data[6].split('=')[1].split(',')[2])
    xfix, yfix, zfix = int(data[7].split('=')[1].split(',')[0]),\
                       int(data[7].split('=')[1].split(',')[1]),\
                       int(data[7].split('=')[1].split(',')[2])

    #  debug parameters
    pf = int(data[9].split('=')[1])
    RunRobot = int(data[10].split('=')[1])
    oneshot = data[11].split('=')[1][:-1]
    PicPlot = int(data[12].split('=')[1])
    Draw_3D = int(data[13].split('=')[1])
    SinglePic = int(data[14].split('=')[1])
    
    
    c_1 = 179  # c_1=0
    mode = 3
    PathFile = ['ADYDAMCP_Path',  # 0 White shoes
                'AFHDVQRU_Path',  # 1 White shoes back
                'CWUYJYDG_Path',  # 2 Black shoes  ##
                'EGQUQCSS_Path',  # 3 Corver
                'HQEHSCGP_Path',  # 4 Black shoes
                'XSWLJFFF_Path',  # 5 Black shoes##
                'QDWVWHMT_Path',  # 6 Tray back
                'YLXEQVFU_Path',  # 7 Tray
                'JEMPECDF_Path',  # 8
                'PQQKUTTO_Path',  # 9
                'DNHUMLHI_Path', # 10
                'MISDKFVP_Path'
               ]
    root = 'path/'
    HeartFile = PathFile[pf].replace('Path', 'Others')
    Fname = time.strftime("%m%d%H%M", time.localtime())
    
    x,y,z = [],[],[]
    Laps = []

    #  src/module/data/algorithm    # 559
    # paPath   = algorithm.analyzePath(pcData, par)[1]
    # pcOthers = algorithm.analyzePath(pcData, par)[2]
    # agData   = algorithm.analyzePath(pcData, par)[3]
    for i in range(len(pcPath)):
        x.append(pcPath[i][0])
        y.append(pcPath[i][1])
        z.append(pcPath[i][2])
        Laps.append(pcPath[i][4])
    
    Hx ,Hy ,Hz  = pcOthers[0][0], pcOthers[0][1], pcOthers[0][2]
    Tx1,Ty1,Tz1 = pcOthers[1][0], pcOthers[1][1], pcOthers[1][2]
    Tx2,Ty2,Tz2 = pcOthers[2][0], pcOthers[2][1], pcOthers[2][2]
    
    #  import by txt
    hh = []
    T1 = []
    T2 = []
    print('File---', PathFile[pf])
    f = open('{}{}.pcd'.format(root, HeartFile), 'r')   ###
    data = f.readlines()
    for i in range(9, len(data)):
        HT = data[i].split(' ')[0:3]
        if i ==10:
            hh = [float(j)*1 for j in HT]
        elif i ==11:
            T1 = [float(j)*1 for j in HT]
        elif i ==12:
            T2 = [float(j)*1 for j in HT]
    
    Hx ,Hy ,Hz  = round(hh[0],2), round(hh[1],2), round(hh[2],2)  # shape heart
    Tx1,Ty1,Tz1 = round(T1[0],2), round(T1[1],2), round(T1[2],2)  # endpoint
    Tx2,Ty2,Tz2 = round(T2[0],2), round(T2[1],2), round(T2[2],2)  # endpoint
    
    # read pcd x y z a b c Laps
    f = open('{}{}.pcd'.format(root, PathFile[pf]), 'r')
    data = f.readlines()
    
    AxisNum = len(data[10].split(' '))
    print('AxisNum:', AxisNum)
    
    for i in range(10, len(data)):
        for j in range(AxisNum-1):
            xyz = float(data[i].split(' ')[j])
            
            if j % AxisNum ==0:
                x.append(round(xyz*1,2))
            elif j % AxisNum ==1:
                y.append(round(xyz*1,2))
            elif j % AxisNum ==2:
                z.append(round(xyz*1,2))
                
            if AxisNum > 3:
    #            if j % AxisNum ==5:
    #                b.append(round(xyz,2))
    #            elif j % AxisNum ==7:
    #                a.append(round(xyz,2))
                if j % AxisNum ==4:
                    Laps.append(int(xyz))
                    
    ##################  if we get Laps No. ####################################
    LapsNum = []
    print('Total points:', len(x))
    for i in range(max(Laps)+1):
        LapsNum.append(Laps.count(i+0))
        print('lap{}: {}'.format(i+1,LapsNum[i]),'ps')
    
    space = []
    for i in range(max(Laps)+1):
        if i == 0:
            space.append(int(LapsNum[i]/(SpaceNum*2)))  # (20*0.67**i)
        else:
            space.append(int(LapsNum[i]/SpaceNum))
    
    ##  build xyz list
    #xyz_co = []
    #for i in range(0, len(x)):
    #    xyz_co.append([x[i],y[i],z[i]])
    
    #  find the longest distance
    def dis_xyz(x, y, z, i, j):
        return ((x[i]-x[j])**2
               +(y[i]-y[j])**2
               +(z[i]-z[j])**2)**0.5
    
    dis_all = []
    for i in range(0,len(x)):
        for j in range(i+1,len(x)):
            dis = dis_xyz(x, y, z, i, j)
            dis_all.append([dis, i, j])
            
    longindex = dis_all.index(max(dis_all))
    print(dis_all[longindex])
    A = dis_all[longindex][1]
    B = dis_all[longindex][2]
    
    Tx1,Ty1 = x[A],y[A]
    Tx2,Ty2 = x[B],y[B]
    
    print('Mid(z), T1(z):', Hz,z[A])
    print('Mid(z), MaxLap1:', Hz,min(z[:LapsNum[0]]))
    if Hz < min(z[:LapsNum[0]]):
        SprayAngle = -int(SprayAngle*0.5)
        print('Convex')
    
    feed = []
    for k in range(len(LapsNum)-1):   # len(LapsNum)-1
        dis = []
        for i in range(sum(LapsNum[:k+1]),len(x)):
            if k == 0:
                dis.append(dis_xyz(x, y, z, sum(LapsNum[:k+1])-1, i))
            else:
                dis.append(dis_xyz(x, y, z, feed[k-1], i))
        feed.append(dis.index(min(dis)) + sum(LapsNum[:k+1]))
    
    def newLoop(k):
        for i in range(len(LapsNum)):
            if i == 0:
                nL = k[0 : sum(LapsNum[:i+1])]
                
            elif i == len(LapsNum):
                 nL = nL + k[feed[i-1] :     ] + k[sum(LapsNum[:i]) : feed[i-1]]
            else:
                nL = nL + k[feed[i-1] : sum(LapsNum[:i+1])-0] + k[sum(LapsNum[:i]) : feed[i-1]]
        return nL
    
    x_new = newLoop(x)
    y_new = newLoop(y)
    z_new = newLoop(z)
    print(np.mean(z[LapsNum[0]:int(LapsNum[0]*1.1)]), np.mean(z[:int(LapsNum[0]*0.1)]))
    
    # rotate angle
    dx = ((Tx1 - Hx)**2)**0.5
    dy = ((Ty1 - Hy)**2)**0.5
    the = np.arctan(dx/dy)
    an = round(the*180/np.pi,1)
    
    if (Tx1 - Hx)*(Ty1 - Hy) > 0:
        an = -an
    
    print('Robot fix angle:', an)
    
    if mode == 3:
        an = 0
    
    def get_point(x,y,cX,cY,angle):
        new_x = (x-cX) * np.cos(np.pi/180.0*angle) - (y-cY) * np.sin(np.pi/180.0*angle) + cX
        new_y = (x-cX) * np.sin(np.pi/180.0*angle) + (y-cY) * np.cos(np.pi/180.0*angle) + cY
        return round(new_x,2), round(new_y,2)
    
    x_new_an = []
    y_new_an = []
    for i in range(len(x_new)):
        x_an, y_an = get_point(x_new[i], y_new[i], Hx, Hy, -an)
        x_new_an.append(x_an)
        y_new_an.append(y_an)
    
    Tx1_an, Ty1_an = get_point(Tx1, Ty1, Hx, Hy, -an)
    Tx2_an, Ty2_an = get_point(Tx2, Ty2, Hx, Hy, -an)
    
    x_sp, y_sp, z_sp = [],[],[]
    b_sp, a_sp = [],[]
    x90, y90 = [],[]
    phi_list = []
    def PathData(lapA, lapB, sp):
        for i in range(lapA, lapB, sp):
            x_sp.append(x_new_an[i])
            y_sp.append(y_new_an[i])
            z_sp.append(z_new[i])
            x90.append(-y_new_an[i])
            y90.append( x_new_an[i])
            
            b_sp.append(round(vg.signed_angle(
                    np.array([+y_new_an[i],
                              -x_new_an[i],
                                  z_new[i]]),
                    np.array([+Hy, -Hx, Hz]),
                    look = vg.basis.y),2))
        
            a_sp.append(round(vg.signed_angle(
                    np.array([+y_new_an[i],
                              -x_new_an[i],
                                  z_new[i]]),
                    np.array([+Hy, -Hx, Hz]),
                    look = vg.basis.x),2))
            
            dx = x_new_an[i] - Hx
            dy = y_new_an[i] - Hy
            phi = np.arctan(dx/dy)
            phi_deg = phi*180/np.pi
            if dx < 0 and dy > 0:
                k = phi_deg+360-90
                if k<0:
                    k = k+360
                phi_list.append(k)
            elif dx > 0 and dy > 0:
                k = phi_deg-90
                if k<0:
                    k = k+360
                phi_list.append(k)
            elif dx > 0 and dy < 0:
                k = phi_deg+180-90
                if k<0:
                    k = k+360
                phi_list.append(k)
            elif dx < 0 and dy < 0:
                k = phi_deg+180-90
                if k<0:
                    k = k+360
                phi_list.append(k)
    
    if max(Laps) >= 3:
        LapThrowAway = 0
    else:
        LapThrowAway = 1
        
    for i in range(max(Laps) + LapThrowAway):   # throw away last lap
        PathData(sum(LapsNum[:i]), sum(LapsNum[:i+1]), space[i])
    
    #   mapping axis to robot
    RobotX, RobotY, RobotZ = [],[],[]
    for i in range(0, len(x_sp)):
        RobotX.append(round((rx - y_sp[i] + xfix),3))
        RobotY.append(round((ry - x_sp[i] + yfix),3))
        RobotZ.append(round((rz - z_sp[i] + zfix),3))
    
    a_list = []
    b_list = []
    
    a_max = +(SprayAngle/abs(max(a_sp)))
    a_min = +(SprayAngle/abs(min(a_sp)))
    b_max = -(SprayAngle/abs(max(b_sp)))
    b_min = -(SprayAngle/abs(min(b_sp)))
    
    
    def WCmsg(p1,p2):
        MsgTitle = {"dsID":"HCRemoteCommand","emptyList":"0",
                    "dsData":[{"camID":"0","data":[]}]}
        for i in range(p1,p2):
            MsgSub={"oneshot":"1","action":"10",
                     "xpos":"","ypos":"","zpos":"",
                     "upos":"","vpos":"","wpos":"",
                     "speed":"50.0","delay":"0.0","smooth":"9"}
            if a_sp[i]>=0 and b_sp[i]<0:
                a_1 = round(+180-(a_sp[i]*a_max-0),1)
                b_1 = round(   0-(b_sp[i]*b_min),1)
         
            elif a_sp[i]>=0 and b_sp[i]>=0:
                a_1 = round(+180-(a_sp[i]*a_max-0),1)
                b_1 = round(   0-(b_sp[i]*b_max),1)
        
            elif a_sp[i]<0 and b_sp[i]>=0:
                a_1 = round(-180-(a_sp[i]*a_min+0),1)
                b_1 = round(   0-(b_sp[i]*b_max),1)
                
            elif a_sp[i]<0 and b_sp[i]<0:
                a_1 = round(-180-(a_sp[i]*a_min+0),1)
                b_1 = round(   0-(b_sp[i]*b_min),1)
    
            MsgValue=[oneshot, "10", str(RobotX[i]), str(RobotY[i]), str(RobotZ[i]),
                       str(a_1), str(b_1), str(c_1), speed, "0.0", "9"]
            MsgTitle["dsData"][0]["data"].append(dict(zip(MsgSub, MsgValue)))
            a_list.append(a_1)
            b_list.append(b_1)
        return MsgTitle
    
    
    msg = []
    for i in range(0,len(RobotX),20):
        if i+20 > len(RobotX):
            msg.append(WCmsg(i, len(RobotX)))
        else:
            msg.append(WCmsg(i, i+20))
    return msg,RunTime

# =============================================================================
# #   make json txt
# json_txt = open("{}{}_{}.txt".format(root, PathFile[pf], Fname), "w")
# json_txt.writelines(str({"dsID":"HCRemoteCommand",
#                          "emptyList":"1","dsData":[{"camID":"0","data":
#                        [{"oneshot":"1","action":"10",
#                          "xpos":str(rx),"ypos":str(ry),"zpos":str(rz),
#                          "upos":"0","vpos":"-6","wpos":"178",
#                          "speed":"10.0","delay":"0.0","smooth":"9"}]}]}
#                        ).replace(" ",""))
# json_txt.writelines(str({"dsID":"www.hc-system.com.RemoteMonitor",
#                          "reqType":"command","cmdData":["startButton"]}
#                        ).replace(" ",""))
# for i in range(len(msg)):
#     json_txt.writelines(str(msg[i]).replace(" ",""))
# json_txt.close()
# =============================================================================

if __name__=='__main__':
#    for pf in range(len(pathfile)):
#        main(pf)
#        time.sleep(15)
    main(pcPath, pcOthers, agData)




