#!/usr/bin/env python3.9
#Bu kod engel gördüğünde aracı durdurur
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, Int32

def lane_callback(msg):
    global current_lane
    current_lane = msg.data

def callback(data):
    global scan
    scan = data.ranges

if __name__ == "__main__":
    rospy.init_node('obstacle_detect')

    # rospy.wait_for_message("/current_lane", timeout=10)
    rospy.Subscriber('/scan', LaserScan, callback, queue_size=10)
    rospy.Subscriber('/current_lane', Int32, lane_callback, queue_size=10)

    # Veriables
    scan = None
    current_lane = None
    rate = rospy.Rate(1)

    # Publishers
    obstacle_publisher = rospy.Publisher("/obstacle/obstacledetection_cmd", Bool, queue_size=10)

while not rospy.is_shutdown():
    if scan is not None:
        obstacle_detected = False
        for angle_index in range (0,1285):
            distance = scan[angle_index]
            if distance != float('inf'):
                if angle_index <= 72 and angle_index >= 0 and distance < 2:
                    rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance}")
                    obstacle_detected = True
                    obstacle_publisher.publish(True)
                if angle_index <= 1285 and angle_index > 1180 and distance < 2:
                    rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance}")
                    obstacle_detected = True
                    obstacle_publisher.publish(True)        
                           
        if not obstacle_detected:
            obstacle_publisher.publish(False)
    rate.sleep()
