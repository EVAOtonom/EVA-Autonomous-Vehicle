import time
from ultralytics import YOLO
import cv2
import math
import AKS_Communication as aks
stm = aks.STM_Communication("/dev/ttyUSB0")
model=YOLO('/home/otonom/Desktop/otonom-git/EVA-Autonomous-Vehicle/levha-tespiti/29.01best.pt')

class_names = ['20', '30', 'dur', 'durak', 'girisyok', 'ilerisag', 'ilerisol', 'kirmizi', 'park', 'parkyasak', 'sag', 'sagadonulmez', 'sari', 'sol', 'soladonulmez', 'yesil', 'engellipark', 'tasitrafiginekapali', 'yayagecidi', 'kavsak', 'ikiliyon', 'tersengellipark','parkYapilmaz']
    
def object_detection(device):
    cap = cv2.VideoCapture(device)
    cap.set(3, 640)
    cap.set(4, 480)
    frame_count = 0
    detection_interval = 4
    while True:
        if not cap.isOpened():
            print("Kamera açılamadı!")
            break
        success, frame = cap.read()
        if not success:
            print("frame okunamadı!")
            break
        frame_count += 1
        if frame_count % detection_interval == 0:
            results = model(frame, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    # put box in cam
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                    confidence = math.ceil((box.conf[0]*100))/100
                    detected_sign = class_names[int(box.cls[0])]
                    
                    cv2.putText(frame, detected_sign+" "+str(confidence), [x1, y1], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        cv2.imshow('EVA Object Detection', frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

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
        
stm.send_command(aks.Register.RESET_ENCODER,1)
stm.send_command(aks.Register.MOTOR_POWER,2)
object_detection(0)
