# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 10:53:38 2020

@author: Sunny
"""

def plot(PathFile,pf,
         x,y,
         x_new,y_new,
         x_new_an,y_new_an,
         x_sp,y_sp,z_sp,
         a_sp,b_sp,
         a_list,b_list,
         Laps,LapsNum,
         Tx1,Ty1,Tx2,Ty2,
         Tx1_an,Ty1_an,Tx2_an,Ty2_an,
         Hx,Hy,
         ):
    
    import matplotlib.pyplot as plt
    Draw_3D = 0
    #  path view  x --> (-x)
    fig = plt.figure(frameon=False, figsize=(36,16))
    ax1 = fig.add_subplot(1,4,1)
    ax2 = fig.add_subplot(1,4,2)
    ax3 = fig.add_subplot(1,4,3)
    ax4 = fig.add_subplot(1,4,4)
    
    for i in range(len(x)):
        if i>0:
            px = [-x[i],-x[i-1]]
            py = [ y[i], y[i-1]]
            ax1.plot(px, py, color='b')
            
            px = [-x_new[i],-x_new[i-1]]
            py = [ y_new[i], y_new[i-1]]
            ax2.plot(px, py, color='g')
            
            px = [-x_new_an[i],-x_new_an[i-1]]
            py = [ y_new_an[i], y_new_an[i-1]]
            ax3.plot(px, py, color='g')
            
    for i in range(len(x_sp)):
        ax3.scatter(-x_sp[i], y_sp[i], color='r')
        ax4.scatter(-x_sp[i], y_sp[i], color='r')
        
    #    label = '{}'.format(round(phi_list[i],1))
        label = '{}'.format(str(a_sp[i])+'\n'+str(b_sp[i]))
        ax3.text(-x_sp[i], y_sp[i]+2, label, fontsize=8)
        label = '{}'.format(str(a_list[i])+'\n'+str(b_list[i]))
        ax4.text(-x_sp[i], y_sp[i]+2, label, fontsize=8)
        
        if i >0:
            px = [-x_sp[i],-x_sp[i-1]]
            py = [ y_sp[i], y_sp[i-1]]
            ax4.plot(px, py, color='g')
    
    def Plt_Scat_Txt(ax,x,y,color,lwidth,txt,fsize):
        ax.scatter(x, y, color=color, linewidth=lwidth)
        ax.text(x, y-6, txt, fontsize=fsize)
    
    LapColor = ['r','g','b']
    LapName = ['lap1','lap2','lap3','lap4','lap5','lap6','lap7']
    
    for i in range(max(Laps)):
        Plt_Scat_Txt(ax1, -x[sum(LapsNum[:i+1])-1],
                           y[sum(LapsNum[:i+1])-1],
                           LapColor[0], 8, LapName[i], 8)
        
        Plt_Scat_Txt(ax2, -x_new[sum(LapsNum[:i+1])-1],
                           y_new[sum(LapsNum[:i+1])-1],
                           LapColor[0], 8, LapName[i], 8)
        
        Plt_Scat_Txt(ax3, -x_new_an[sum(LapsNum[:i+1])-1],
                           y_new_an[sum(LapsNum[:i+1])-1],
                           LapColor[0], 8, LapName[i], 8)
    
        Plt_Scat_Txt(ax4, -x_new_an[sum(LapsNum[:i+1])-1],
                           y_new_an[sum(LapsNum[:i+1])-1],
                           LapColor[0], 8, LapName[i], 8)
    
    Plt_Scat_Txt(ax2,-Tx1, \
                      Ty1,'c',10,'T1',8)
    Plt_Scat_Txt(ax2,-Tx2, \
                      Ty2,'c',10,'T2',8)
    Plt_Scat_Txt(ax2,-Hx, \
                      Hy,'m',10,'Mid',8)
    
    Plt_Scat_Txt(ax3,-Tx1_an, \
                      Ty1_an,'c',10,'T1',8)
    Plt_Scat_Txt(ax3,-Tx2_an, \
                      Ty2_an,'c',10,'T2',8)
    Plt_Scat_Txt(ax3,-Hx, \
                      Hy,'m',10,'Mid',8)
    
    Plt_Scat_Txt(ax4,-Hx, \
                      Hy,'m',10,'Mid',8)
    
    
    ax3.plot([- max(x), -min(x)],
             [+Hy, +Hy], color='y', linewidth=1)
    ax3.plot([-Hx, -Hx],
             [+ min(y),  max(y)], color='y', linewidth=1)
    
    ax4.plot([- max(x), -min(x)],
             [+Hy, +Hy], color='y', linewidth=1)
    ax4.plot([-Hx, -Hx],
             [+ min(y),  max(y)], color='y', linewidth=1)
    
    def setXYaxis(ax):
        ax.set_xlabel('X', fontsize=16)
        ax.set_ylabel('Y', fontsize=16)
        ax.axis("equal")
    
    setXYaxis(ax1)
    setXYaxis(ax2)
    setXYaxis(ax3)
    setXYaxis(ax4)
    
    #plt.axis('scaled')
    plt.title('{}'.format(PathFile[pf]), fontsize=26)
    #    plt.savefig('{}{}{}.png'.format(root, PathFile[pf], Fname)\
    #                ,bbox_inches='tight')
    #    plt.close(fig)
    
    if Draw_3D==1:
        from mpl_toolkits.mplot3d import Axes3D
        
        fig3D = plt.figure(frameon=False, figsize=(80,30), dpi=20)
        ax3D = Axes3D(fig3D)
        for i in range(len(x_sp)):
            ax3D.scatter(-x_sp[i], y_sp[i], z_sp[i], color='b', linewidth=20)
            px=[-x_sp[i],-x_sp[i-1]]
            py=[ y_sp[i], y_sp[i-1]]
            pz=[ z_sp[i], z_sp[i-1]]
            ax3D.plot(px, py, pz, color='g')
        
        ax3D.tick_params(axis='both', which='major', labelsize=40)
        ax3D.tick_params(axis='both', which='minor', labelsize=40)
        
        ax3D.set_xlabel('X', fontsize=60)
        ax3D.set_ylabel('Y', fontsize=60)
        ax3D.set_zlabel('Z', fontsize=60)
        
        #ax3D.set_xlim3d(min(x_sp), max(x_sp))
        #ax3D.set_ylim3d(min(y_sp), max(y_sp))
        #ax3D.set_zlim3d(min(z_sp), max(z_sp))
        #ax3D.set_aspect("equal")
        #ax3D.view_init(elev=30,azim=150)
        #ax3D.view_init(elev= 90,azim=180)
        
        
        #def rotate(angle):
        #    ax3D.view_init(azim=angle)
        #rot_animation = animation.FuncAnimation(fig3D, rotate, frames=np.arange(0,362,2),interval=100)
        #rot_animation.save('path/rotation.gif', dpi=80, writer='imagemagick')
        
        
        ax3D.view_init(45, -175)
        plt.draw()
        plt.pause(10)
        
        #plt.savefig('{}{}Path2Robot{}_3D.png'.format(root, pathfile, Fname)\
        #            ,bbox_inches='tight')
        plt.show()
        #plt.close(fig3D)


# =============================================================================
#     if SinglePic==1:
#         # single plot
#         plt.figure(frameon=False, figsize=(36,16))
#         for i in range(945):
#             if i>0:
#                 px = [-x[i],-x[i-1]]
#                 py = [ y[i], y[i-1]]
#                 plt.plot(px, py, color='b')
#                 
#         Plt_Scat_Txt(plt,-x[LapsNum[0]-1],y[LapsNum[0]-1],'r',10,'670',12)
#         Plt_Scat_Txt(plt,-x[671],y[671],'r',10,'671',12)
#         Plt_Scat_Txt(plt,-x[1114],y[1114],'g',6,'1114',12)
#         Plt_Scat_Txt(plt,-x[943],y[943],'b',3,'943',12)
#         Plt_Scat_Txt(plt,-x[944],y[944],'b',3,'944',12)
#         Plt_Scat_Txt(plt,-x[886],y[886],'b',3,'886',12)
#         plt.axis('equal')
#     #    plt.savefig('{}{}7788{}.png'.format(root, pathfile, Fname)\
#     #                ,bbox_inches='tight')
# =============================================================================
