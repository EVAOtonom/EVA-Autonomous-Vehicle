import time
from rplidar import RPLidar

PORT_NAME = 'COM3'
distances = [0]
lidar = RPLidar(PORT_NAME, baudrate=256000, timeout=2)
sayac=0

try:
    time.sleep(0.5)
    for bool, lazer_gucu, angle, distance in lidar.iter_measurments(max_buf_meas=500):
        if 360 > angle > 350 or 10>angle>0:             #TESTTE KONTROL ET              #ARACIN ORTA NOKTASINI TARAR
            sayac+=1
            print(distance,sayac)
            
except:
    print("EXCEPT ÇALISTI LİDAR BAŞLAMADI...")
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()