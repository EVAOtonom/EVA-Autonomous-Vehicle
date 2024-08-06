#!/usr/bin/env python3.9
#Bu kod engel gördüğünde engelden kaçar!
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, Float32, Int8, Float64
import time

def decision_callback(msg):
    global sign_detected
    sign_detected = msg.data

def sign_callback(msg):
    global detected_sign_number
    detected_sign_number= msg.data

def callback(msg):
    global scan
    scan = msg.ranges

def current_lane_check(msg):
    global current_lane
    current_lane = msg.data

def read_odometer(msg):
    global traveled_distance
    traveled_distance = msg.data

def EscapeLeft():
    global obstacle_detected
    if scan is not None:
        obstacle_detected = False
        for angle_index in range (89,160):
            distance = scan[angle_index]
            if distance != float('inf'):
                if (89 <= angle_index <= 160 and distance < 450 ) :
                    rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance}")
                    obstacle_publisher.publish(True)
                    obstacle_detected = True
                    avoidance_obstacle(current_lane, 1)



def EscapeRight():
    global obstacle_detected
    if scan is not None:
        obstacle_detected = False
        for angle_index in range (428,152):
            distance = scan[angle_index]
            if distance != float('inf'):
                if (120 <= angle_index <= 543 and distance < 450 ):
                    rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance}")
                    obstacle_publisher.publish(True)
                    obstacle_detected = True
                    avoidance_obstacle(1, 1)

def avoidance_obstacle(current_lane, kacinma):

    if current_lane == 0 and kacinma == 0:
        rospy.loginfo(f"SOLDAN KACIS BASLIYOR")
        brake_pub.publish(1)
        time.sleep(0.2)
        rospy.loginfo(f"TEKER SAGA DONDU")
        steering_pub.publish(40)
        right_signal.publish(True)
        time.sleep(0.2)
        brake_pub.publish(0)
        distance_temp = traveled_distance
        while traveled_distance - distance_temp < 150:
            EscapeLeft()
            print(traveled_distance-distance)
        time.sleep(1)
        right_signal.publish(False)
        while traveled_distance - distance_temp < 250:
            rospy.loginfo("beklemeye girdi 2.5 ---- 0-0")
        time.sleep(1)
        steering_pub.publish(-40)
        left_signal.publish(True)
        time.sleep(1)
        distance_temp = traveled_distance
        while traveled_distance - distance_temp < 250:
            rospy.loginfo("Beklemeye girdi 2.5 AMA ALT TARAF ----  0-0")
        time.sleep(2)
        left_signal.publish(False)
        obstacle_detected = False
        obstacle_publisher.publish(obstacle_detected)



    elif current_lane == 0 and kacinma == 1:
        rospy.loginfo(f"SOLDAN Büyük KACIS BASLIYOR")
        time.sleep(0.2)
        left_signal.publish(True)
        steering_pub.publish(-40)
        time.sleep(0.5)
        brake_pub.publish(0)
        distance_temp = traveled_distance
        while traveled_distance - distance_temp < 2.2:
            rospy.loginfo("Beklemeye girdi 2.2M ----  0-1")
        time.sleep(1)
        left_signal.publish(False)
        obstacle_detected = False
        obstacle_publisher.publish(obstacle_detected)



    elif current_lane == 1 and kacinma == 0:
        rospy.loginfo(f"SAGDAN KACIS BASLIYOR")
        brake_pub.publish(1)
        time.sleep(0.2)
        rospy.loginfo(f"TEKER SOLA DONDU")
        steering_pub.publish(-35)
        time.sleep(0.2)
        #left_signal.publish(True)
        time.sleep(0.2)
        brake_pub.publish(0)
        time.sleep(0.2)
        distance_temp = traveled_distance
        while traveled_distance - distance_temp < 150:
            EscapeRight()
            print(traveled_distance-distance_temp)
        time.sleep(0.2)
        left_signal.publish(False)
        time.sleep(0.2)
        distance_temp = traveled_distance
        while traveled_distance - distance_temp < 250:
            rospy.loginfo("Beklemeye girdi 2.5M ----  1-0")
        time.sleep(0.2)
        steering_pub.publish(30)
        time.sleep(0.2)
        right_signal.publish(True)
        time.sleep(0.2)
        distance_temp = traveled_distance
        while traveled_distance - distance_temp < 250:
            rospy.loginfo("Beklemeye girdi 2.5M AMA ALT TARAFTA ----  1-0")
        time.sleep(0.2)
        steering_pub.publish(0)
        time.sleep(0.2)
        right_signal.publish(False)
        time.sleep(0.2)
        obstacle_detected = False
        obstacle_publisher.publish(obstacle_detected)
        time.sleep(0.2)




    elif current_lane == 1 and kacinma == 1:
        rospy.loginfo(f"SAGDAN 2. KACIS BASLIYOR")
        left_signal.publish(True)
        steering_pub.publish(-40)
        time.sleep(0.2)
        brake_pub.publish(0)
        distance_temp = traveled_distance
        while traveled_distance - distance_temp < 2.6:
            rospy.loginfo("Beklemeye girdi 2.6M ----  1-1")
        time.sleep(0.5)
        left_signal.publish(False)
        obstacle_detected = False
        obstacle_publisher.publish(obstacle_detected)


if __name__ == "__main__":
    rospy.init_node('obstacle_detector_node')
    
    #Variables
    scan = None
    current_lane = 1
    traveled_distance = 0
    obstacle_detected = False
    sign_detected = False
    detected_sign_number = False
    HelperArray3 = []
    rate = rospy.Rate(1)

    #Subscribers
    rospy.Subscriber('/scan', LaserScan, callback, queue_size=10)
    rospy.Subscriber("/lane_track/current_lane", Int8, current_lane_check) # 0 sol 1 sağ
    rospy.Subscriber('/stm/read_odometer', Float32, read_odometer)
    rospy.Subscriber('/decision_algorithm/detection_control', Bool, decision_callback)
    rospy.Subscriber("/sign_detector/detected_sign_number", Int8, sign_callback)

    #Publishers
    left_signal = rospy.Publisher('/stm/left_signal', Bool, queue_size= 10)
    right_signal = rospy.Publisher('/stm/right_signal', Bool, queue_size=10)
    obstacle_publisher = rospy.Publisher("/obstacle_detector/obstacle_detection", Bool, queue_size=10)
    steering_pub = rospy.Publisher("/stm/steering_angle", Int8, queue_size=100)
    throttle_pub = rospy.Publisher("/stm/motor_power", Int8, queue_size=100)
    brake_pub = rospy.Publisher("/stm/brake", Bool, queue_size=100)
    throttle_pub.publish(1)
    obstacle_publisher.publish(obstacle_detected)

    # #Şerit Takibi Bekleme
    # rospy.loginfo("Waiting for 'lane_track_node' service...")
    # rospy.wait_for_message("/lane_track/current_lane",Int8,timeout=100) # Şerit takibinin mevcut şerit bilgisini göndermesini bekler.
    # rospy.loginfo("'lane_track_node' service is now available.")    

    while not rospy.is_shutdown():
        if not sign_detected:
            if scan is not None:
                obstacle_detected = False
                for angle_index in range (0,1285):
                    distance = scan[angle_index]
                    if distance != float('inf'):
                        if angle_index <= 72 and angle_index >= 0 and distance < 2.5:
                            rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance}")
                            obstacle_detected = True
                            obstacle_publisher.publish(True)
                            avoidance_obstacle(1, 0)
                            break
                        if angle_index <= 1285 and angle_index > 1180 and distance < 2.5:
                            rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance}")
                            obstacle_detected = True
                            obstacle_publisher.publish(True)
                            avoidance_obstacle(1, 0)
                            break
            rate.sleep()
