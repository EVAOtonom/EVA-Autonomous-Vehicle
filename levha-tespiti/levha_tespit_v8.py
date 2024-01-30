#!/usr/bin/env python3.9
import time
from ultralytics import YOLO
import cv2
import AKS_Communication as aks

stm = aks.STM_Communication("/dev/ttyUSB0")
model=YOLO('/home/otonom/otonom_ws/src/levha_tespiti/src/29.01best.pt')

def hareket_durak():
        
        stm.send_command(aks.Register.RESET_ENCODER,1)        
        stm.send_command(aks.Register.MOTOR_POWER,0)        
        stm.send_command(aks.Register.STEERING_ANGLE,40)        
        time.sleep(2) 
        stm.send_command(aks.Register.MOTOR_POWER,2)        

                
        while stm.read_data(aks.Register.READ_ODOMETER) < 250:
            continue 
        
        stm.send_command(aks.Register.RESET_ENCODER,1)        
        stm.send_command(aks.Register.MOTOR_POWER,0)        
        stm.send_command(aks.Register.STEERING_ANGLE,-40)     
        time.sleep(4) 
        
        stm.send_command(aks.Register.MOTOR_POWER,2)        


        while stm.read_data(aks.Register.READ_ODOMETER) < 250:
            continue 

        stm.send_command(aks.Register.RESET_ENCODER,1)        
        stm.send_command(aks.Register.MOTOR_POWER,0)        
        stm.send_command(aks.Register.STEERING_ANGLE,0)     
        time.sleep(10)
      
        stm.send_command(aks.Register.STEERING_ANGLE,-40)        
        time.sleep(2) 
        stm.send_command(aks.Register.MOTOR_POWER,2)        

                
        while stm.read_data(aks.Register.READ_ODOMETER) < 300:
            continue 
        
        stm.send_command(aks.Register.RESET_ENCODER,1)        
        stm.send_command(aks.Register.MOTOR_POWER,0)        
        stm.send_command(aks.Register.STEERING_ANGLE,40)     
        time.sleep(4) 
        
        stm.send_command(aks.Register.MOTOR_POWER,2)        


        while stm.read_data(aks.Register.READ_ODOMETER) < 210:
            continue 

        stm.send_command(aks.Register.RESET_ENCODER,1)        
        stm.send_command(aks.Register.MOTOR_POWER,0)        
        stm.send_command(aks.Register.STEERING_ANGLE,0)     
        time.sleep(1)

def hareket_sag():
        
        stm.send_command(aks.Register.RESET_ENCODER,1)  
        stm.send_command(aks.Register.MOTOR_POWER,0)        
        stm.send_command(aks.Register.STEERING_ANGLE,40)     
        time.sleep(3) 
        
        stm.send_command(aks.Register.MOTOR_POWER,2)    

        while stm.read_data(aks.Register.READ_ODOMETER) < 430:
            continue 

        stm.send_command(aks.Register.RESET_ENCODER,1)
        stm.send_command(aks.Register.MOTOR_POWER,0)  
        stm.send_command(aks.Register.STEERING_ANGLE,0)    
        time.sleep(3) 

        stm.send_command(aks.Register.MOTOR_POWER,2) 

        while stm.read_data(aks.Register.READ_ODOMETER) < 200:
            continue 

        stm.send_command(aks.Register.RESET_ENCODER,1)        
        stm.send_command(aks.Register.MOTOR_POWER,0) 

def camera():
    cap = cv2.VideoCapture(2)
    
    while cap.isOpened() :
        ret,frame = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        results=model(frame)

        for r in results:
            a=r.boxes
            b = a.cls.cpu()
            c=b.numpy()
            if c == 3 :
                hareket_durak()
            elif c == 10 :
                hareket_sag()

    cap.release()
    cv2.destroyAllWindows()

stm.send_command(aks.Register.RESET_ENCODER,1)
stm.send_command(aks.Register.MOTOR_POWER,2)
camera()
