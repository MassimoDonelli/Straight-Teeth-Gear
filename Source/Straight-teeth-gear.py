# -*- coding: utf-8 -*-
# .. Massimo Donelli, April 2025, V1.0 ..
# .. Import Library ..
import os
import math
import numpy as np
import ezdxf
# .. Import Graph libraries ..
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
# .. Define Functions ..
def InsertData():
   T_RATIO = 1
   Z=0
   print("Do you want to design a Gear o a single Wheel (G/W):")
   GearWheelFLag=str(input("G or W:"))
   print(GearWheelFLag)
   if((GearWheelFLag == "W") or (GearWheelFLag == "w")):
       # .. Insert the pressure ration theta (15°/20°) ..
       PRESSURE_ANGLE_THETA = float(input("Insert the pressure ration theta (15°/20°):"))
       # .. Insert the wheel module ..
       print("Normalized gear module:", np.arange(0.5,3.75,0.25))
       MODULE = float(input("Insert the gear module [mm]:")) 
       # .. Insert the teeth number Z ..
       Z = int(input("Insert the teeth number:"))
       # .. Insert the Axis diameter ..
       AXIS_HOLE = float(input("Insert the main axis hole diameter [mm]:")) 
   elif((GearWheelFLag == "G") or (GearWheelFLag == "g")):  
       # .. Insert the required transmission ratio ..
       T_RATIO = float(input("Insert the transmission ratio R=Z2/Z1:"))
       # .. Insert the pressure ration theta (15°/20°) ..
       PRESSURE_ANGLE_THETA = float(input("Insert the pressure ration theta (15°/20°):"))
       # .. Insert the wheel module ..
       print("Normalized gear module:", np.arange(0.5,3.75,0.25))
       MODULE = float(input("Insert the gear module [mm]:"))
       # .. Insert the Axis diameter ..
       AXIS_HOLE = float(input("Insert the main axis hole diameter [mm]:"))
   else:
      print("Error Wrong choice!")
      exit(0)    
   return GearWheelFLag,PRESSURE_ANGLE_THETA,MODULE,Z,T_RATIO,AXIS_HOLE
#
def GearTeethNumberEstimation(PRESSURE_ANGLE_THETA, T_RATIO): 
    # .. Estimate minimum Z1 number ..
    Z1 = 2 / ((math.sqrt(pow(T_RATIO,2)+ (1 + 2*T_RATIO) * pow(math.sin(PRESSURE_ANGLE_THETA* math.pi/180),2))) - T_RATIO)
    MIN_Z1 = math.floor(Z1)
    print(MIN_Z1)
    Z2 = T_RATIO*MIN_Z1
    #
    if(Z2 - math.floor(Z2) == 0.0):
       Z1 = math.floor(Z1)
       Z2 = T_RATIO*Z1    
    else:
       MAX_Z1 = math.ceil(Z1)
       print(MAX_Z1)   
       Z1 = MAX_Z1
       Z2 = T_RATIO*MAX_Z1   
    return Z1,int(Z2)
# .. Gear geometrical shape visualization .. 
def VisualizeGearGeometry(XG1,YG1,XG2,YG2,INTER_AXIS,AXIS_HOLE):
   for I_X_FOR in range(len(XG2)):
      XG2[I_X_FOR] += INTER_AXIS 
   # .. Plot Driven Wheel geometry ..    
   plt.plot(XG2, YG2,'-',linewidth='1.5',color='black') 
   # .. Plot Hole geometry .. 
   # 
   X=[]
   Y=[] 
   POINTS = 10000
   ANGULAR_STEP = 2*math.pi/POINTS
   for I_X_FOR in range(POINTS+1):
      t = ANGULAR_STEP*I_X_FOR
      X.append((AXIS_HOLE/2)*(math.sin(t))+INTER_AXIS)
      Y.append((AXIS_HOLE/2)*(math.cos(t)))    
   # .. Plot axis hole ..    
   plt.plot(X, Y,'-',linewidth='1.5',color='black')
   #
   ALPHA=0.06108652381980153     # .. for Z2/Z1<3 it is only a misalignment in the visualization 
   for I_X_FOR in range(len(XG1)):   
    XG1[I_X_FOR] = XG1[I_X_FOR]*math.cos(ALPHA) - YG1[I_X_FOR]*math.sin(ALPHA)
    YG1[I_X_FOR] = XG1[I_X_FOR]*math.sin(ALPHA) + YG1[I_X_FOR]*math.cos(ALPHA)

   plt.plot(XG1, YG1,'-',linewidth='1.5',color='black') 
   # .. Plot Hole geometry .. 
   # 
   X=[]
   Y=[] 
   POINTS = 10000
   ANGULAR_STEP = 2*math.pi/POINTS
   for I_X_FOR in range(POINTS+1):
      t = ANGULAR_STEP*I_X_FOR
      X.append((AXIS_HOLE/2)*(math.sin(t)))
      Y.append((AXIS_HOLE/2)*(math.cos(t)))    
   # .. Plot axis hole ..    
   plt.plot(X, Y,'-',linewidth='1.5',color='black')
   #  
   plt.axis('equal')
   plt.grid()  
   plt.title('Gear Geometry')
   plt.show()
# .. Wheel geometrical shape visualization .. 
def VisualizeWheelGeometry(XC,YC,XG,YG,AXIS_HOLE):
   for I_X_FOR in range(len(XG)):
      XG[I_X_FOR] += XC
      YG[I_X_FOR] += YC 
   # .. Plot Teeth geometry ..    
   plt.plot(XG, YG,'-',linewidth='1.5',color='black') 
   # .. Plot Hole geometry .. 
   # 
   X=[]
   Y=[] 
   POINTS = 10000
   ANGULAR_STEP = 2*math.pi/POINTS
   for I_X_FOR in range(POINTS+1):
      t = ANGULAR_STEP*I_X_FOR
      X.append((AXIS_HOLE/2)*(math.sin(t))+XC)
      Y.append((AXIS_HOLE/2)*(math.cos(t))+YC)    
   # .. Plot axis hole ..    
   plt.plot(X, Y,'-',linewidth='1.5',color='black') 
   plt.axis('equal')
   plt.grid()  
   plt.title('Gear Geometry')
   plt.show()
# .. Design a cicloid teeth  ..   
def StraightToothGear(MODULE,Z,PRESSURE_ANGLE,FLAG_VISUALIZATION):
      RAD = (math.pi/180)
      PRIMITIVE_DIAMETER = MODULE*Z
      EXTERNAL_DIAMETER = PRIMITIVE_DIAMETER + 2*MODULE
      FOOT_DIAMETER = PRIMITIVE_DIAMETER - 2.5*MODULE
      BASE_DIAMETER = PRIMITIVE_DIAMETER*math.cos(PRESSURE_ANGLE*RAD)
      BETA_ANGLE = (360/Z)/4
      DELTA_ANGLE = (math.sqrt(pow(PRIMITIVE_DIAMETER,2)-pow(BASE_DIAMETER,2))/BASE_DIAMETER)*(180/math.pi)-PRESSURE_ANGLE
      #
      print("_______________________________________")
      print("PRIMITIVE_DIAMETER:",PRIMITIVE_DIAMETER)
      print("EXTERNAL_DIAMETER:",EXTERNAL_DIAMETER)
      print("FOOT_DIAMETER:",FOOT_DIAMETER)
      print("BASE_DIAMETER:",BASE_DIAMETER)
      print("BETA:",BETA_ANGLE)
      print("DELTA:",DELTA_ANGLE)
      POINTS = 100#00
      X=[]
      Y=[]
      ANGULAR_STEP = 2*math.pi/POINTS 
      for I_X_FOR in range(POINTS+1):
         t = ANGULAR_STEP*I_X_FOR
         X.append((PRIMITIVE_DIAMETER/2)*(math.sin(t)))
         Y.append((PRIMITIVE_DIAMETER/2)*(math.cos(t)))    
      if(FLAG_VISUALIZATION == 1):
      # .. Plot primitive circle ..    
       plt.plot(X, Y,'--',linewidth='0.5',color='black') 
      # 
      X=[]
      Y=[] 
      for I_X_FOR in range(POINTS+1):
         t = ANGULAR_STEP*I_X_FOR
         X.append((EXTERNAL_DIAMETER/2)*(math.sin(t)))
         Y.append((EXTERNAL_DIAMETER/2)*(math.cos(t)))    
      if(FLAG_VISUALIZATION == 1):
      # .. Plot external circle ..    
       plt.plot(X, Y,'--',linewidth='0.5',color='red')
      X=[]
      Y=[] 
      for I_X_FOR in range(POINTS+1):
         t = ANGULAR_STEP*I_X_FOR
         X.append((FOOT_DIAMETER/2)*(math.sin(t)))
         Y.append((FOOT_DIAMETER/2)*(math.cos(t)))    
      if(FLAG_VISUALIZATION == 1):
      # .. Plot foot circle ..    
       plt.plot(X, Y,'--',linewidth='0.5',color='blue') 
      # 
      X=[]
      Y=[] 
      for I_X_FOR in range(POINTS+1):
         t = ANGULAR_STEP*I_X_FOR
         X.append((AXIS_HOLE/2)*(math.sin(t)))
         Y.append((AXIS_HOLE/2)*(math.cos(t)))    
      if(FLAG_VISUALIZATION == 1):
      # .. Plot axis hole ..    
       plt.plot(X, Y,'-',linewidth='1.5',color='black') 
      # 
      X=[]
      Y=[] 
      for I_X_FOR in range(POINTS+1):
         t = ANGULAR_STEP*I_X_FOR
         X.append((BASE_DIAMETER/2)*(math.sin(t)))
         Y.append((BASE_DIAMETER/2)*(math.cos(t)))    
      if(FLAG_VISUALIZATION == 1):
      # .. Plot base circle ..    
       plt.plot(X, Y,'-',linewidth='0.5',color='green') 
      # .. Add the well .. 
      X=[]
      Y=[] 
      #
      if((FOOT_DIAMETER/2)<(BASE_DIAMETER/2)):
          DOWN_LIMIT = (BASE_DIAMETER/2)
          #
          X.append((FOOT_DIAMETER/2)*math.sin(90*RAD))
          Y.append((FOOT_DIAMETER/2)*math.cos(90*RAD))   
          #
          X.append((FOOT_DIAMETER/2)*math.sin((90+BETA_ANGLE)*RAD))
          Y.append((FOOT_DIAMETER/2)*math.cos((90+BETA_ANGLE)*RAD))
      else:
          DOWN_LIMIT = (FOOT_DIAMETER/2)
          #
          X.append(DOWN_LIMIT*math.sin(90*RAD))
          Y.append(DOWN_LIMIT*math.cos(90*RAD))   
          #
          X.append(DOWN_LIMIT*math.sin((90+BETA_ANGLE)*RAD))
          Y.append(DOWN_LIMIT*math.cos((90+BETA_ANGLE)*RAD))
       # 
      for I_X_FOR in range(POINTS+1):
         t = ANGULAR_STEP*I_X_FOR
         XD=(DOWN_LIMIT*(math.cos(-t-BETA_ANGLE*RAD)-t*math.sin(-t-BETA_ANGLE*RAD)))
         YD=(DOWN_LIMIT*(math.sin(-t-BETA_ANGLE*RAD)+t*math.cos(-t-BETA_ANGLE*RAD))) 
         if(pow(YD,2)+pow(XD,2) <= pow((EXTERNAL_DIAMETER/2),2)):
           X.append(XD)
           Y.append(YD) 
      # .. Estimates the second evolvent circle .. 
      ALPHA = -3*BETA_ANGLE-DELTA_ANGLE
      for I_X_FOR in range(POINTS+1,0,-1):
         t = ANGULAR_STEP*I_X_FOR
         XD=(DOWN_LIMIT*(math.cos(t)+t*math.sin(t)))
         YD=(DOWN_LIMIT*(math.sin(t)-t*math.cos(t))) 
         XR = XD*math.cos(ALPHA*RAD)-YD*math.sin(ALPHA*RAD)
         YR = XD*math.sin(ALPHA*RAD)+YD*math.cos(ALPHA*RAD)
         if(pow(YD,2)+pow(XD,2) <= pow((EXTERNAL_DIAMETER/2),2)):
           X.append(XR)
           Y.append(YR)   
      if((FOOT_DIAMETER/2)<(BASE_DIAMETER/2)):
           XD=(FOOT_DIAMETER/2)
           YD= 0  
           X.append(XD*math.cos(ALPHA*RAD))#-YD*math.sin(ALPHA*RAD)
           Y.append(XD*math.sin(ALPHA*RAD))#+YD*math.cos(ALPHA*RAD)
      # .. Now Rotate the teeth ..
      XT=[]
      YT=[]
      for I_X_FOR in range(Z):      
         ALPHA -= 360/Z
         for J_X_FOR in range(len(X)):
            XT.append(X[J_X_FOR]*math.cos(ALPHA*RAD)-Y[J_X_FOR]*math.sin(ALPHA*RAD))
            YT.append(X[J_X_FOR]*math.sin(ALPHA*RAD)+Y[J_X_FOR]*math.cos(ALPHA*RAD))
      # .. CLose the loop ..
      XT.append(XT[0])
      YT.append(YT[0])
      if(FLAG_VISUALIZATION == 1):
       plt.plot(XT, YT,'-',linewidth='1.5',color='black')    
       STR = "Straight-tooth-gear Z:" + str(Z) + " m:" + str(MODULE)
       plt.title(STR)
       plt.axis('equal')
       plt.legend(["Primitive", "Head", "Foot", "Gear","Base"])
       plt.grid()
       plt.show() 
      return XT,YT
# .. Save DWG file format ..
def ExportCAD(FILE_NAME,XG,YG,AXIS_HOLE):
   PATH = "/Users/massimo/Desktop/Progetti/Straight-tooth-gear/"
   # .. Define the file and model space ..
   doc = ezdxf.new(setup=True)
   msp = doc.modelspace()
   # .. Drawing wheel structure ..
   for I_X_FOR in range(len(XG)-1):
      msp.add_line((XG[I_X_FOR],YG[I_X_FOR]),(XG[I_X_FOR+1],YG[I_X_FOR+1]))
   # .. Drawing the wheel hole ..
   X=[]
   Y=[]
   POINTS = 100
   ANGULAR_STEP = 2*math.pi/POINTS
   for I_X_FOR in range(POINTS+1):
      t = ANGULAR_STEP*I_X_FOR
      X.append((AXIS_HOLE/2)*(math.sin(t)))
      Y.append((AXIS_HOLE/2)*(math.cos(t)))
   for I_X_FOR in range(POINTS):
      msp.add_line((X[I_X_FOR],Y[I_X_FOR]),(X[I_X_FOR+1],Y[I_X_FOR+1]))
   doc.saveas(PATH + FILE_NAME + ".dxf")      
# .. Main Program ..
if __name__ == '__main__':
 #
 os.system('clear all')
 #
 print("__________________________________")
 print("Phase 1 Insert Data")
 GearWheelFLag,PRESSURE_ANGLE_THETA,MODULE,Z,T_RATIO,AXIS_HOLE = InsertData()   
 print("End ...")
 print("__________________________________")   
 if((GearWheelFLag == 'W') or (GearWheelFLag == 'w')):
      print("Phase 2 Estimates the wheel geometry")
      XG,YG = StraightToothGear(MODULE,Z,PRESSURE_ANGLE_THETA,1)
      VisualizeWheelGeometry(0,0,XG,YG,AXIS_HOLE)
      print("End ...")
      print("__________________________________")
      print("Do you want to save the CAD of the wheel (Y/N)?")
      DUMMY_FLAG = input()
      if((DUMMY_FLAG == 'Y') or (DUMMY_FLAG == 'y')):
         print("Save the CAD file as dwg ")
         FILE_NAME = input("Insert output file-name:")
         ExportCAD(FILE_NAME,XG,YG,AXIS_HOLE)
 elif((GearWheelFLag == 'G') or (GearWheelFLag == 'g')):
      print("Phase 2 Estimates the gear geometry")
      Z1,Z2 = GearTeethNumberEstimation(PRESSURE_ANGLE_THETA, T_RATIO)
      STEP = (MODULE*math.pi)
      ADDENDUM = MODULE
      DEDENDUM = 1.25*MODULE 
      TOOTH_HEIGH = ADDENDUM + DEDENDUM
      # .. Estimate primary diameter ..
      PRIMARY_DIAMETER_Z1 = MODULE*Z1
      PRIMARY_DIAMETER_Z2 = MODULE*Z2
      # .. Estimate external diameter ..
      EXTERNAL_DIAMETER_Z1 = PRIMARY_DIAMETER_Z1+(2*MODULE)
      EXTERNAL_DIAMETER_Z2 = PRIMARY_DIAMETER_Z2+(2*MODULE)
      # .. Estimate foot diameter ..
      FOOT_DIAMETER_Z1 = PRIMARY_DIAMETER_Z1-(2*DEDENDUM)
      FOOT_DIAMETER_Z2 = PRIMARY_DIAMETER_Z2-(2*DEDENDUM)
      # .. Estimate the inter axis ..
      INTER_AXIS = (PRIMARY_DIAMETER_Z1+PRIMARY_DIAMETER_Z2)/2   
      print("Teeth Number of the two wheels (Z1 Driver, Z2 Conducted Wheel):","Z1 = ",Z1," Z2 = ",Z2)
      print("Transmission Ratio:",Z2/Z1)
      print("Primary diameter Z1:",PRIMARY_DIAMETER_Z1)
      print("Primary diameter Z2:",PRIMARY_DIAMETER_Z2)
      #
      print("External diameter Z1:",EXTERNAL_DIAMETER_Z1)
      print("External diameter Z2:",EXTERNAL_DIAMETER_Z2)
      #
      print("Step P:",STEP)
      print("Addendum:",ADDENDUM)
      print("Dedendum:",DEDENDUM)
      print("Tooth Heigh:",TOOTH_HEIGH)
      print("Inter axis distance:",INTER_AXIS)
      # .. Design the Driver Wheel .. 
      XG1,YG1 = StraightToothGear(MODULE,Z1,PRESSURE_ANGLE_THETA,0)
      XG2,YG2 = StraightToothGear(MODULE,Z2,PRESSURE_ANGLE_THETA,0)
      VisualizeGearGeometry(XG1,YG1,XG2,YG2,INTER_AXIS,AXIS_HOLE)
      print("End ...")
      print("__________________________________")
      print("Do you want to save the CAD of the wheel (Y/N)?")
      DUMMY_FLAG = input()
      if((DUMMY_FLAG == 'Y') or (DUMMY_FLAG == 'y')):
         print("Save the CAD files of Driven and Conducted wheels as dwg:")
         FILE_NAME = input("Insert output file-name:")
         ExportCAD(FILE_NAME+'_Z1',XG1,YG1,AXIS_HOLE)
         ExportCAD(FILE_NAME+'_Z2',XG2,YG2,AXIS_HOLE)
      