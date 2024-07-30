import time
from rplidar import RPLidar
from STM_Communication import send_to_STM

PORT_NAME = 'COM8'
distances = [0]
lidar = RPLidar(PORT_NAME, baudrate=256000, timeout=2)

hangiSerit=1 #1 -> sağ şerit 0 -> sol şerit

try:
    time.sleep(0.5)
    send_to_STM(2,2)
    for bool, lazer_gucu, angle, distance in lidar.iter_measurments(max_buf_meas=500):
        if 360 > angle > 350 or 10>angle>0:             #TESTTE KONTROL ET              #ARACIN ORTA NOKTASINI TARAR
            if distance !=0 :
                if distance < 3000:
                    print(distance)
                    if hangiSerit==0:
                        send_to_STM(2,0)#motor gücünü kes
                        send_to_STM(0,40)#tekerlek açısını 40 derece çevir
                        send_to_STM(2,2)#motora güç ver
                        time.sleep(5)
                        send_to_STM(0,0)#motordan güçü kes
                        send_to_STM(2,0)#teker açısını 0 yap

                    elif hangiSerit==1:
                        send_to_STM(2,0)#motor gücünü kes
                        send_to_STM(0,-40)#tekerlek açısını 40 derece çevir
                        send_to_STM(2,2)#motora güç ver
                        time.sleep(5)
                        send_to_STM(0,0)#motordan güçü kes
                        send_to_STM(2,0)#teker açısını 0 yap


            
except:
    print("EXCEPT ÇALISTI LİDAR BAŞLAMADI...")
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()