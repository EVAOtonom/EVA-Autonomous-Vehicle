#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan

def lidar_callback(data):
    rospy.loginfo("Received lidar data: %f", data.ranges[0])

def lidar_subscriber():
    rospy.init_node('lidar_subscriber', anonymous=True)
    rospy.Subscriber('lidar_scan', LaserScan, lidar_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        lidar_subscriber()
    except rospy.ROSInterruptException:
        pass