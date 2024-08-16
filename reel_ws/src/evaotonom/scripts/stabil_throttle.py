#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32, Int8

# Global değişkenler
current_velocity = 0.0
brake_status = 0  # Varsayılan olarak frenin aktif olduğunu varsayıyoruz

# Motor gücünü yayınlayacağımız publisher
motor_power_pub = None

def velocity_callback(msg):
    global current_velocity
    current_velocity = msg.data

def brake_callback(msg):
    global brake_status
    brake_status = msg.data

def control_motor_power():
    global current_velocity, brake_status, motor_power_pub
    
    if brake_status == 1:
        # Fren aktifse motor gücü 0 olur
        motor_power_pub.publish(Int8(0))
    else:
        # Fren serbestken hız kontrolü yapılır
        if current_velocity > 3.2:
            # Hız 3 km/h üstündeyse motor gücü 0 olur
            motor_power_pub.publish(Int8(0))
        elif current_velocity < 2.6:
            # Hız 2.5 km/h altındaysa motor gücü 6 olur
            motor_power_pub.publish(Int8(7))

if __name__ == '__main__':
    rospy.init_node('speed_control_node')

    # Motor gücü publisher'ı başlat
    motor_power_pub = rospy.Publisher('/stm/motor_power', Int8, queue_size=1)

    # Abonelikleri başlat
    rospy.Subscriber('/vehicle/velocity_kmh', Float32, velocity_callback)
    rospy.Subscriber('/vehicle/brake', Int8, brake_callback)

    # Rate belirleme (10 Hz)
    rate = rospy.Rate(1)  # 10 Hz

    # Ana döngü
    while not rospy.is_shutdown():
        control_motor_power()
        rate.sleep()
