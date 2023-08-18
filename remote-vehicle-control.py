import pygame
import aks_communication
import time
#gear=0 ise ileri gear=1 ise geri
steeringAngle = gear = brake = gas = 0

class func:
    
    def disengage_clutch():
        func.stop_motor()
        func.straighten_wheels()
        func.release_brake()
    
    def release_brake():
        aks_communication.sendToArduino("b0\n")
        time.sleep(0.5)
        brake=0
        
    def apply_brake():
        aks_communication.sendToArduino("b1\n")
        time.sleep(0.5)
        brake=1
    
    def straighten_wheels():
        global steeringAngle
        aks_communication.sendToArduino("t0\n")
        steeringAngle=0
        time.sleep(0.5)
        
    def put_reverse():
        global gear
        aks_communication.sendToArduino("r\n")
        time.sleep(0.2)
        gear=1
        
    def put_gear():
        global gear
        aks_communication.sendToArduino("r\n")
        # acil stop e mi?
        gear=0
        time.sleep(0.2) 
        
    def stop_motor():
        global gas
        aks_communication.sendToArduino("w0\n")
        time.sleep(0.2)
        gas=0
        
    def go():
        global gas,brake,gear
        if gear==1:
            func.put_gear()
        elif brake==1:
            func.release_brake()
        elif gas==0:
            print("ileri marş")
            aks_communication.sendToArduino("w80\n")
            gas=1
        elif gas==1:
            print("ileri marş")
        
    def go_back():
        global gas
        func.stop_motor()
        func.apply_brake()
        func.put_reverse()
        func.release_brake()
        if gas==0:
            print("geri marş")
            aks_communication.sendToArduino("w80\n")
        else:
            print("geri marş")
        
    def turn_right():
        global steeringAngle
        if steeringAngle>-95:
            steeringAngle=steeringAngle-5
            strSteeringAngle="t"+str(steeringAngle)+"\n"
            print("Açı: ",strSteeringAngle)
            aks_communication.sendToArduino(steeringAngle) 
        else:
            pass
        
    def turn_left():
        if steeringAngle<95:
            steeringAngle=steeringAngle+5
            strSteeringAngle="t"+str(steeringAngle)+"\n"
            print("Açı: ",strSteeringAngle)
            aks_communication.sendToArduino(steeringAngle)
        else:
            pass
            
        
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

vehicle=func()

start=False
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button==7:
                start=not start
                print("Kumanda devrede")
                while start:
                    for event in pygame.event.get():
                        if event.type == pygame.JOYBUTTONDOWN:
                            if event.button==7:
                                print("Kumanda devredışı")
                                start=not start
                                break
                            print("Butona basildi:",event.button)
                        if event.type == pygame.JOYAXISMOTION:
                            if event.axis == 0:  # Sol/Sağ eksen (x ekseni)
                                if event.value < -0.5:
                                    func.turn_left()
                                elif event.value > 0.5:
                                    func.turn_right()
                            elif event.axis == 1:  # Yukarı/Aşağı eksen (y ekseni)
                                if event.value < -0.5:
                                    func.go()
                                elif event.value > 0.5:
                                    func.go_back()