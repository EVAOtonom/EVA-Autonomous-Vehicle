#!/usr/bin/env python3.9
#Bu kod engel gördüğünde engelden kaçar!
#Current_lane 1 ise sağ 0 ise sol
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, Float32, Int8
import time

def engel_kapat_callback(msg):
    global stop_avoidance
    stop_avoidance = msg.data

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
        while traveled_distance < 230:
            pass
        brake_pub.publish(1)
        time.sleep(2)
        reset_odom.publish(1)
        time.sleep(0.5)
        steering_pub.publish(-40)
        time.sleep(4)
        left_signal.publish(5)
        time.sleep(0.5)
        brake_pub.publish(0)
        time.sleep(0.5)
        print("KENDIMI DUZLUYORUM 0-0")
        while traveled_distance < 300:
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
        while traveled_distance < 180:
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
        rospy.loginfo(f"SOLDAN BÜYÜK KAÇIŞ BAŞLIYOR 0-1")
        left_signal.publish(5)
        time.sleep(0.5)
        brake_pub.publish(0)
        time.sleep(2)
        rospy.loginfo("Beklemeye girdi 4M ----  0-1")
        while traveled_distance < 500:
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
        while traveled_distance < 275:
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
        while traveled_distance < 326:
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
        while traveled_distance < 200:
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
        while traveled_distance < 500:
            pass
        time.sleep(0.5)
        steering_pub.publish(0)
        time.sleep(2)
        obstacle_detected = False
        obstacle_publisher.publish(obstacle_detected)
def birinci_bolge_karari_sag():
    global obstacle_detected, scan, sign_detected
    if not sign_detected:
        if scan is not None:
            obstacle_detected = False
            for angle_index in range (0,81):
                distance = scan[angle_index]
                if distance != float('inf'):
                    if 3 < distance < 3.1:
                        rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 2. BÖLGE Sağ")
                        ikinci_bolge_karari_sag()
                        return True
    return False
def birinci_bolge_karari_sol():
    global obstacle_detected, scan, sign_detected
    if not sign_detected:
        if scan is not None:
            obstacle_detected = False
            for angle_index in range (1204,1285):
                distance = scan[angle_index]
                if distance != float('inf'):
                    if 3 < distance < 3.4:
                        rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 2. BÖLGE Sol")
                        ikinci_bolge_karari_sol()
                        return True
    return False 
def ikinci_bolge_karari_sag():
    global obstacle_detected, scan, sign_detected
    if not sign_detected:
        if scan is not None:
            obstacle_detected = False
            for angle_index in range (82,185):
                distance = scan[angle_index]
                if distance != float('inf'):
                    if 3.1 < distance < 4.5: #3. bölgede de engel var
                        rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 3. BÖLGE Sağ")
                        ucuncu_bolge_karari_sag()
                        return
            rospy.loginfo("3. BÖLGE TEMİZ SOLDAN SAĞA KAÇIŞ YAPILIYOR Sağ")
            obstacle_detected = True
            obstacle_publisher.publish(True)
            avoidance_obstacle(current_lane, 0) #DEĞERLER GİRİLECEK KAÇIŞ OLACAK
def ikinci_bolge_karari_sol():
    global obstacle_detected, scan, sign_detected
    if not sign_detected:
        if scan is not None:
            obstacle_detected = False
            for angle_index in range (1102,1203):
                distance = scan[angle_index]
                if distance != float('inf'):
                    if 3.1 < distance < 4.5: #3. bölgede de engel var
                        rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 3. BÖLGE Sol")
                        ucuncu_bolge_karari_sol()
                        return
            rospy.loginfo("3. BÖLGE TEMİZ SOLDAN SAĞA KAÇIŞ YAPILIYOR Sol")
            obstacle_detected = True
            obstacle_publisher.publish(True)
            avoidance_obstacle(current_lane, 0) #DEĞERLER GİRİLECEK KAÇIŞ OLACAK
def ucuncu_bolge_karari_sag():
    global obstacle_detected, scan, sign_detected
    if not sign_detected:
        if scan is not None:
            obstacle_detected = False
            for angle_index in range (186,215):
                distance = scan[angle_index]
                if distance != float('inf'):
                    if 4.5 < distance < 6:
                        rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 4. BÖLGE Sağ")
                        obstacle_detected = True
                        obstacle_publisher.publish(True)
                        avoidance_obstacle(current_lane, 1) #GENİŞ KAÇIŞ OLACAK
                        return
            rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 4. BÖLGE Sağ")
            obstacle_detected = True
            obstacle_publisher.publish(True)
            avoidance_obstacle(current_lane, 1) #GENİŞ KAÇIŞ OLACAK 
def ucuncu_bolge_karari_sol():
    global obstacle_detected, scan, sign_detected
    if not sign_detected:
        if scan is not None:
            obstacle_detected = False
            for angle_index in range (1067,1101):
                distance = scan[angle_index]
                if distance != float('inf'):
                    if (1067 <= angle_index <= 1101) and  4.5 < distance < 6:
                        rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 4. BÖLGE Sol")
                        obstacle_detected = True
                        obstacle_publisher.publish(True)
                        avoidance_obstacle(current_lane, 1) #GENİŞ KAÇIŞ OLACAK
                        return
            rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 4. BÖLGE Sol")
            obstacle_detected = True
            obstacle_publisher.publish(True)
            avoidance_obstacle(current_lane, 1) #GENİŞ KAÇIŞ OLACAK    


if __name__ == "__main__":
    rospy.init_node('obstacle_detector_node')
    
    #Variables
    scan = None
    current_lane = 1
    traveled_distance = 0
    stop_avoidance = False
    obstacle_detected = False
    sign_detected = False
    viraj_detected = False
    detected_sign_number = False
    HelperArray3 = []
    rate = rospy.Rate(5)

    #Subscribers
    rospy.Subscriber('/scan', LaserScan, callback, queue_size=1)
    rospy.Subscriber("/lane_track/current_lane", Int8, current_lane_check, queue_size=1) # 0 sol 1 sağ
    rospy.Subscriber('/stm/read_odometer', Float32, read_odometer, queue_size=1)
    rospy.Subscriber('/engel_kapat', Bool , engel_kapat_callback, queue_size=1)

    #Publishers
    reset_odom = rospy.Publisher('/stm/reset_odometer', Bool, queue_size=1)
    left_signal = rospy.Publisher('/stm/left_signal', Int8, queue_size= 1)
    right_signal = rospy.Publisher('/stm/right_signal', Int8, queue_size=1)
    obstacle_publisher = rospy.Publisher("/engel_var_mi", Bool, queue_size=1)
    steering_pub = rospy.Publisher("/stm/steering_angle", Int8, queue_size=1)
    throttle_pub = rospy.Publisher("/stm/motor_power", Int8, queue_size=1)
    brake_pub = rospy.Publisher("/stm/brake", Bool, queue_size=1)
    obstacle_publisher.publish(obstacle_detected)

    # #Şerit Takibi Bekleme
    rospy.loginfo("Waiting for 'lane_track_node' service...")
    rospy.wait_for_message("/lane_track/current_lane",Int8,timeout=100) # Şerit takibinin mevcut şerit bilgisini göndermesini bekler.
    rospy.loginfo("'lane_track_node' service is now available.")
       
    while not rospy.is_shutdown():
        if not sign_detected and not stop_avoidance:
            if scan is not None:
                obstacle_detected = False
                for angle_index in range (0,1285):
                    distance = scan[angle_index]
                    if distance != float('inf'):
                        if ((1265 <= angle_index <= 1285) or (0 <= angle_index <= 20)) and  (3 < distance < 3.1):
                            rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} ARA BÖLGE")
                            if current_lane == 1:
                                karar = birinci_bolge_karari_sag()
                            else:
                                karar = birinci_bolge_karari_sol()
                            if not karar:
                                avoidance_obstacle(current_lane,0)
                            break
                        elif (0 <= angle_index <= 81) and  (3 < distance < 3.1) and (current_lane == 0):
                            rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 1. BÖLGE SOL")
                            birinci_bolge_karari_sol()
                            break
                        elif(1205 <= angle_index <= 1285) and (3 <= distance <= 3.1) and (current_lane == 1):
                            rospy.loginfo(f" ENGEL VAR açı:{angle_index} mesafe: {distance} 1. BÖLGE SAĞ")
                            birinci_bolge_karari_sag()
                            break
                        
        rate.sleep()
