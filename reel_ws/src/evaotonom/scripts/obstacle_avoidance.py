#!/usr/bin/env python3.9
#Bu kod engel gördüğünde engelden kaçar!
#Current_lane 1 ise sağ 0 ise sol
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, Float32, Int8
import time

def decision_callback(msg):
    global sign_detected
    sign_detected = msg.data

def callback(msg):
    global scan
    scan = msg.ranges

def current_lane_check(msg):
    global current_lane
    current_lane = msg.data

def read_odometer(msg):
    global traveled_distance
    traveled_distance = msg.data


def avoidance_obstacle(current_lane, kacinma):
    if current_lane == 0 and kacinma == 0:
        brake_pub.publish(1)
        time.sleep(2)
        rospy.loginfo("SOLDAN KACIS 0-0")
        reset_odom.publish(1)
        time.sleep(0.5)
        steering_pub.publish(40)
        time.sleep(2)
        right_signal.publish(5)
        time.sleep(0.5)
        brake_pub.publish(0)
        time.sleep(2)
        print("SAĞ SERIDE GECIYORUM  0-0")
        while traveled_distance < 300:
            pass
        brake_pub.publish(1)
        time.sleep(2)
        reset_odom.publish(1)
        time.sleep(0.5)
        steering_pub.publish(-40)
        time.sleep(4)
        right_signal.publish(5)
        time.sleep(0.5)
        brake_pub.publish(0)
        time.sleep(0.5)
        print("KENDIMI DUZLUYORUM 0-0")
        while traveled_distance < 450:
            pass
        brake_pub.publish(1)
        time.sleep(2)
        reset_odom.publish(1)
        time.sleep(0.5)
        steering_pub.publish(0)
        time.sleep(2.5)
        brake_pub.publish(0)
        time.sleep(2)
        print("BITIRDIM SOL SERITTE DEVAM EDIYORUM 0-0")
        while traveled_distance < 250:
            pass
        brake_pub.publish(1)
        time.sleep(2)
        obstacle_detected = False
        obstacle_publisher.publish(obstacle_detected)


    elif current_lane == 0 and kacinma == 1: #GENİŞ KAÇIŞ SOLDAN SAĞ
        brake_pub.publish(1)
        time.sleep(2)
        rospy.loginfo("SOLDAN KACIS 0-1")
        reset_odom.publish(1)
        time.sleep(0.5)
        steering_pub.publish(40)
        time.sleep(2.5)
        right_signal.publish(5)
        time.sleep(0.5)
        rospy.loginfo(f"SOLDAN BÜYÜK KAÇIŞ BAŞLIYOR 0-1")
        reset_odom.publish(1)
        time.sleep(0.5)
        left_signal.publish(2)
        time.sleep(0.5)
        brake_pub.publish(0)
        time.sleep(2)
        rospy.loginfo("Beklemeye girdi 4M ----  0-1")
        while traveled_distance < 400:
            pass
        time.sleep(0.5)
        steering_pub.publish(0)
        time.sleep(2)
        obstacle_detected = False
        obstacle_publisher.publish(obstacle_detected)

    elif current_lane == 1 and kacinma == 0:
        brake_pub.publish(1)
        time.sleep(2)
        rospy.loginfo("SAGDAN KACIS")
        reset_odom.publish(1)
        time.sleep(0.5)
        steering_pub.publish(-40)
        time.sleep(2.5)
        left_signal.publish(5)
        time.sleep(0.5)
        throttle_pub.publish(2)
        time.sleep(0.5)
        brake_pub.publish(0)
        time.sleep(2)
        print("SOL SERIDE GECIYORUM")
        while traveled_distance < 300:
            pass
            # brake_pub.publish(1)
            # time.sleep(2)
        reset_odom.publish(1)
        time.sleep(0.5)
        steering_pub.publish(40)
        time.sleep(4)
            # brake_pub.publish(0)
            # time.sleep(2)
        print("KENDIMI DUZLUYORUM")
        while traveled_distance < 450:
            pass
            # brake_pub.publish(1)
            # time.sleep(2)
        reset_odom.publish(1)
        time.sleep(0.5)
        steering_pub.publish(-40)
        time.sleep(2.5)
            # brake_pub.publish(0)
            # time.sleep(2)
        print("BITIRDIM SOL SERITTE DEVAM EDIYORUM")
        while traveled_distance < 250:
            pass
            # brake_pub.publish(1)
            # time.sleep(2)
        obstacle_detected = False
        obstacle_publisher.publish(obstacle_detected)

    elif current_lane == 1 and kacinma == 1:
        brake_pub.publish(1)
        time.sleep(2)
        rospy.loginfo("SAGDAN KACIS")
        reset_odom.publish(1)
        time.sleep(0.5)
        steering_pub.publish(-40)
        time.sleep(2.5)
        left_signal.publish(5)
        time.sleep(0.5)
        throttle_pub.publish(2)
        rospy.loginfo(f"SAGDAN 2. KACIS BASLIYOR")
        reset_odom.publish(1)
        time.sleep(2)
        left_signal.publish(2)
        time.sleep(4)
        brake_pub.publish(0)
        time.sleep(2)
        rospy.loginfo("Beklemeye girdi 4M ----  1-1")
        while traveled_distance < 400:
            pass
        time.sleep(0.5)
        steering_pub.publish(0)
        time.sleep(2)
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
    rate = rospy.Rate(5)

    #Subscribers
    rospy.Subscriber('/scan', LaserScan, callback, queue_size=10)
    rospy.Subscriber("/lane_track/current_lane", Int8, current_lane_check) # 0 sol 1 sağ
    rospy.Subscriber('/stm/read_odometer', Float32, read_odometer)
    rospy.Subscriber('/decision_algorithm/detection_control', Bool, decision_callback)

    #Publishers
    reset_odom = rospy.Publisher('/stm/reset_odometer', Bool, queue_size=10)
    left_signal = rospy.Publisher('/stm/left_signal', Int8, queue_size= 10)
    right_signal = rospy.Publisher('/stm/right_signal', Int8, queue_size=10)
    obstacle_publisher = rospy.Publisher("/obstacle_detector/obstacle_detection", Bool, queue_size=10)
    steering_pub = rospy.Publisher("/stm/steering_angle", Int8, queue_size=100)
    throttle_pub = rospy.Publisher("/stm/motor_power", Int8, queue_size=100)
    brake_pub = rospy.Publisher("/stm/brake", Bool, queue_size=100)
    obstacle_publisher.publish(obstacle_detected)

    # #Şerit Takibi Bekleme
    rospy.loginfo("Waiting for 'lane_track_node' service...")
    rospy.wait_for_message("/lane_track/current_lane",Int8,timeout=100) # Şerit takibinin mevcut şerit bilgisini göndermesini bekler.
    rospy.loginfo("'lane_track_node' service is now available.")
   
    def birinci_bolge_karari_sag():
        global obstacle_detected
        while not rospy.is_shutdown():
            if not sign_detected:
                if scan is not None:
                    obstacle_detected = False
                    for angle_index in range (0,1285):
                        distance = scan[angle_index]
                        if distance != float('inf'):
                            if (0 <= angle_index <= 81) and  3 < distance < 3.4:
                                rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 2. BÖLGE ")
                                ikinci_bolge_karari_sag()
                            else:
                                pass
    def birinci_bolge_karari_sol():
        global obstacle_detected
        while not rospy.is_shutdown():
            if not sign_detected:
                if scan is not None:
                    obstacle_detected = False
                    for angle_index in range (0,1285):
                        distance = scan[angle_index]
                        if distance != float('inf'):
                            if (1204 <= angle_index <= 1285) and  3 < distance < 3.4:
                                rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 2. BÖLGE ")
                                ikinci_bolge_karari_sol()
                            else:
                                pass
    def ikinci_bolge_karari_sag():
        global obstacle_detected
        while not rospy.is_shutdown():
            if not sign_detected:
                if scan is not None:
                    obstacle_detected = False
                    for angle_index in range (0,1285):
                        distance = scan[angle_index]
                        if distance != float('inf'):
                            if (82 <= angle_index <= 185) and  3.5 < distance < 5.5: #3. bölgede de engel var
                                rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 3. BÖLGE ")
                                ucuncu_bolge_karari_sag()
                            else: #1 ve 2de var 3te yok kaçış yapıcak
                                rospy.loginfo("3. BÖLGE TEMİZ SOLDAN SAĞA KAÇIŞ YAPILIYOR")
                                obstacle_detected = True
                                obstacle_publisher.publish(True)
                                avoidance_obstacle(current_lane, 0) #DEĞERLER GİRİLECEK KAÇIŞ OLACAK
    def ikinci_bolge_karari_sol():
        global obstacle_detected
        while not rospy.is_shutdown():
            if not sign_detected:
                if scan is not None:
                    obstacle_detected = False
                    for angle_index in range (0,1285):
                        distance = scan[angle_index]
                        if distance != float('inf'):
                            if (1102 <= angle_index <= 1203) and  3.5 < distance < 5.5: #3. bölgede de engel var
                                rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 3. BÖLGE ")
                                ucuncu_bolge_karari_sol()
                            else: #1 ve 2de var 3te yok kaçış yapıcak
                                rospy.loginfo("3. BÖLGE TEMİZ SOLDAN SAĞA KAÇIŞ YAPILIYOR")
                                obstacle_detected = True
                                obstacle_publisher.publish(True)
                                avoidance_obstacle(current_lane, 0) #DEĞERLER GİRİLECEK KAÇIŞ OLACAK
    def ucuncu_bolge_karari_sag():
        global obstacle_detected
        while not rospy.is_shutdown():
            if not sign_detected:
                if scan is not None:
                    obstacle_detected = False
                    for angle_index in range (0,1285):
                        distance = scan[angle_index]
                        if distance != float('inf'):
                            if (186 <= angle_index <= 215) and  5.5 < distance < 7:
                                rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 4. BÖLGE ")
                                obstacle_detected = True
                                obstacle_publisher.publish(True)
                                avoidance_obstacle(current_lane, 1) #GENİŞ KAÇIŞ OLACAK
                            else:
                                rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 4. BÖLGE ")
                                obstacle_detected = True
                                obstacle_publisher.publish(True)
                                avoidance_obstacle(current_lane, 1) #GENİŞ KAÇIŞ OLACAK                                                              
    def ucuncu_bolge_karari_sol():
        global obstacle_detected
        while not rospy.is_shutdown():
            if not sign_detected:
                if scan is not None:
                    obstacle_detected = False
                    for angle_index in range (0,1285):
                        distance = scan[angle_index]
                        if distance != float('inf'):
                            if (1067 <= angle_index <= 1101) and  5.5 < distance < 7:
                                rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 4. BÖLGE ")
                                obstacle_detected = True
                                obstacle_publisher.publish(True)
                                avoidance_obstacle(current_lane, 1) #GENİŞ KAÇIŞ OLACAK
                            else:
                                rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 4. BÖLGE ")
                                obstacle_detected = True
                                obstacle_publisher.publish(True)
                                avoidance_obstacle(current_lane, 1) #GENİŞ KAÇIŞ OLACAK    
    while not rospy.is_shutdown():
        if not sign_detected:
            if scan is not None:
                obstacle_detected = False
                for angle_index in range (0,1285):
                    distance = scan[angle_index]
                    if distance != float('inf'):
                        if (1203 <= angle_index <= 1285) and  (3 < distance < 3.4) and (current_lane == 1):
                            rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 1. BÖLGE ")
                            birinci_bolge_karari_sag()
    while not rospy.is_shutdown():
        if not sign_detected:
            if scan is not None:
                obstacle_detected = False
                for angle_index in range (0,1285):
                    distance = scan[angle_index]
                    if distance != float('inf'):
                        if (0 <= angle_index <= 81) and  (3 < distance < 3.4) and (current_lane == 0):
                            rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 1. BÖLGE ")
                            birinci_bolge_karari_sol()
                            
                            

            rate.sleep()
