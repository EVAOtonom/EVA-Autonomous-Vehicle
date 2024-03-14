import time

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
    


def karar(class_name,states):
    if class_name == 'durak':
        hareket_durak()
    if class_name == 'sag':
        hareket_sag()
