#!/usr/bin/env python3
import rospy
import time
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16
import AKS_Communication as aks


def lidar_callback(data):
    global last_command_time
    current_time = rospy.get_time()

    if current_time - last_command_time > command_interval:
        # En yakın nesnenin mesafesini bul
        min_distance = min([distance for distance in data.ranges if distance > 0.0])
        
        if min_distance > 0.0 and min_distance < 500.0 : # 2 metreden küçükse
            rospy.loginfo("1 metrenin altında engel tespit edildi: {:.2f}mm".format(min_distance))
            stm.send_command(aks.Register.MOTOR_POWER, 0)
            rospy.loginfo("STM e dur komutu gönderildi...")
        else:
            rospy.loginfo("Mesafe 1 metreden büyük {:.2f}mm".format(min_distance))
            stm.send_command(aks.Register.MOTOR_POWER, 2)

        last_command_time = current_time


def lidar_subscriber():
    global last_command_time
    global stm
    global command_interval

    stm = aks.STM_Communication("/dev/ttyUSB0")
    command_interval = 0.5

    rospy.init_node('lidar_subscriber', anonymous=True)
    last_command_time = rospy.get_time()
    rospy.Subscriber('lidar_scan', LaserScan, lidar_callback)
    rospy.loginfo("Lidar subscriber node is running...")
    rospy.spin()

if __name__ == '__main__':
    try:
        lidar_subscriber()
        rospy.loginfo("Lidar subscriber node is running...")
    except rospy.ROSInterruptException:
        rospy.loginfo("Lidar subscriber node stopped by user.")