#!/usr/bin/env python3.9

#Bu kod engel gördüğünde aracı durdurur
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, Int32

def callback(data):
    global scan
    scan = data.ranges

if __name__ == "__main__":
    rospy.init_node('obstacle_detect')
    rospy.Subscriber('/scan', LaserScan, callback, queue_size=1)
    obstacle_detected = False
    # Veriables
    scan = None
    rate = rospy.Rate(5)

    # Publishers
    brake_pub = rospy.Publisher("/stm/brake", Bool, queue_size=1)
    obstacle_publisher = rospy.Publisher("/engel_var_mi", Bool, queue_size=1)

while not rospy.is_shutdown():
    if scan is not None:
        obstacle_detected = False
        for angle_index in range (0,1285):
            distance = scan[angle_index]
            if distance != float('inf'):
                if ((1250 <= angle_index <= 1284) or (0 <= angle_index <= 35)) and  (2.8 < distance < 2.9 ):  
                    brake_pub.publish(1)
                    obstacle_detected = True
                    obstacle_publisher.publish(True)
    rate.sleep()
