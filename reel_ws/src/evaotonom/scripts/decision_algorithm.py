#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Int8, Float64, Bool, Float32MultiArray, Float32
import time
import os

#sağa ve sola dönüş değiştirildi diğerleride değiştirilecek

def sign_callback(msg):
    global detected_sign_number
    detected_sign_number= msg.data

def read_odometer(msg):
    global distance
    distance = msg.data
    
'''def lane_callback(msg):
    global current_lane
    current_lane = msg.data'''

def kavsak_callback(msg):
    global kavsak_girisi
    kavsak_girisi = msg.data

def position_callback(msg):
    global x1,x2,y1,y2,size,depth
    #x1,y1,x2,y2,depth = None
    if len(msg.data) == 6:
        x1,y1,x2,y2,size,depth = msg.data
        depth = float(depth)
    #print("x1 = {}, x2 = {}, y1 = {}, y2 = {} size = {} depth = {}".format(x1,x2,y1,y2,size,depth))

if __name__ == "__main__":
    rospy.init_node("decision_node")

    #Veriables
    detected_sign_number = None

    distance = 0

    current_lane = 1

    x1, y1, x2, y2, size, depth = (None,)*6

    kavsak_girisi = None

    #ŞERİT TAKİBİ BEKLEME
    # rospy.loginfo("Waiting for 'lane_track_node' service...")
    # rospy.wait_for_message("/lane_track/current_lane",Int8,timeout=100) # Şerit takibinin mevcut şerit bilgisini göndermesini bekler.
    # rospy.loginfo("'lane_track_node' service is now available.")


    #Subscribers
    rospy.Subscriber("/sign_detector/detected_sign_number", Int8, sign_callback)
    rospy.Subscriber('/stm/read_odometer', Float32, read_odometer)
   # rospy.Subscriber('/lane_track/current_lane', Int8, lane_callback)
    rospy.Subscriber('/tabela', Int8, sign_callback , queue_size=10)
    rospy.Subscriber('/position', Float32MultiArray,position_callback ,queue_size=10)
    rospy.Subscriber("/sign_detector/roundabout", Int8 , kavsak_callback)

    #Publishers
    steering_pub = rospy.Publisher("/stm/steering_angle", Int8, queue_size=100)
    brake_pub = rospy.Publisher("/stm/brake", Bool, queue_size=100)
    detection_control = rospy.Publisher("/decision_algorithm/detection_control", Bool, queue_size=10)
    motor_pub = rospy.Publisher("/stm/motor_power", Int8, queue_size=100)
    reset_odom = rospy.Publisher('/stm/reset_odometer', Bool, queue_size=10)

    motor_pub.publish(False)
    detection_control.publish(False)

    while not rospy.is_shutdown():
        if detected_sign_number != None:

            if detected_sign_number == 3: # DURAK KARAR ALGORITMASI
                if current_lane == 1: # SAG SERITTEYSE
                    rospy.loginfo(" @@@@@@@@@@ SAG SERITTEN DURAGA GIRIS BASLIYOR @@@@@@@@@@@@@ ")
                    distance_temp = distance  
                    while distance - distance_temp < 120:  
                        pass
                    detection_control.publish(True) # Tekrar aynı karar algoritmasına girilmemesi için kullanılmaktadır.
                    motor_pub.publish(1)
                    time.sleep(2)
                    brake_pub.publish(1)
                    steering_pub.publish(Float64(28))
                    time.sleep(0.5)
                    motor_pub.publish(0)

                    distance_temp = distance  
                    while distance - distance_temp < 300:  
                        pass

                    motor_pub.publish(1)
                    steering_pub.publish(-40)
                    time.sleep(0.5)
                    motor_pub.publish(0)

                    distance_temp = distance 
                    while distance - distance_temp < 200:
                        pass

                    motor_pub.publish(1)
                    brake_pub.publish(1)
                    steering_pub.publish(Float64(0))
                    time.sleep(10)
                    steering_pub.publish(-28)
                    time.sleep(0.5)
                    motor_pub.publish(0)

                    distance_temp = distance
                    while distance - distance_temp < 270:
                        pass

                    motor_pub.publish(1)
                    steering_pub.publish(Float64(32))
                    time.sleep(0.5)
                    motor_pub.publish(0)

                    distance_temp = distance
                    while distance - distance_temp < 185:
                        pass


                if current_lane == 0:  # SOL SERITTEYSE
                        pass

                detection_control.publish(False) # Tekrar aynı karar algoritmasına girilmemesi için kullanılmaktadır.
                
            elif detected_sign_number == 2: # DUR
                detection_control.publish(True)
                time.sleep(1)
                motor_pub.publish(True)
                brake_pub.publish(1)
                time.sleep(5)
                motor_pub.publish(False)
                time.sleep(5)
                detection_control.publish(False)

            elif detected_sign_number == 23 or detected_sign_number == 15: # YEŞİL IŞIK
                motor_pub.publish(False)

            elif detected_sign_number == 7: # KIRMIZI IŞIK
                motor_pub.publish(True)

            elif detected_sign_number == 8: # PARK 
                if depth is not None:
                    while depth > 337 :
                        print (depth)
                        if x1 == None or x2 == None or size == None:
                            print("None")
                            continue
                        os.system("rosnode kill "+ "lane_track_node")
                        os.system("rosnode kill "+ "obstacle_detector_node")
                        time.sleep(2)
                        sign_midpoint = (x1 + x2) / 2 # Tespit edilen Levhanın orta noktası alınır
                        im_midpoint = size / 2 # Görselin orta noktası alınır
                        steering_angle = (im_midpoint - sign_midpoint)*0.016 # -640 ile 640 arasında olan değer tekerlek açısı için -10 ile 10 arasına çevrilir
                        steering_pub.publish(steering_angle) 
                    time.sleep(0.1)
                    motor_pub.publish(1)
                    time.sleep(0.1)
                    brake_pub.publish(1)
                    detected_sign_number = True
                    rospy.loginfo("Park edildi")
                    detection_control.publish(True)

                    os.system("rosnode kill "+ "stabil_throttle_node")
                    os.system("rosnode kill "+ "sign_detector_node")
                    
                    time.sleep(5)
                
            if detected_sign_number == 13: # sola dönüş
                if current_lane == 1: # sag seritten
                    rospy.loginfo("sagdan sola donus basladı")
                    while distance < 550:
                        print(distance)
                    print("dist bitti")
                    time.sleep(0.5)
                    detection_control.publish(True)
                    steering_pub.publish(-40)
                    time.sleep(0.5)
                    reset_odom.publish(13)
                    while distance < 250:
                        print(distance)
                    steering_pub.publish(0)
                    time.sleep(0.5)
                    reset_odom.publish(13)
                
                elif current_lane == 0: # sol seritten
                    rospy.loginfo("soldan sola donus basladı")
                    distance_temp = distance
                    while distance - distance_temp <650:
                        print(distance)
                    print("dist bitti")
                    time.sleep(1.5)
                    detection_control.publish(True)
                    steering_pub.publish(-40)
                    distance_temp = distance
                    while distance - distance_temp < 280:
                        print(distance - distance_temp)
                    steering_pub.publish(0)
                    motor_pub.publish(0)                    

                detection_control.publish(False)               

            if detected_sign_number == 10: # saga donus
                if current_lane == 1: # sag seritten
                    rospy.loginfo("sagdan saga donus basladı")
                    while distance - distance_temp <550:
                        print(distance)
                    print("dist bitti")
                    time.sleep(0.5)
                    detection_control.publish(True)                       
                    steering_pub.publish(40)
                    time.sleep(0.5)
                    reset_odom.publish(13)
                    while distance < 250:
                        print(distance)
                    steering_pub.publish(0)
                    time.sleep(0.5)
                    reset_odom.publish(13)
                    
                elif current_lane == 0: # sol seritten
                        distance_temp = distance
                        while distance - distance_temp <650:
                            print(distance)
                        print("dist bitti")
                        time.sleep(1.5)
                        rospy.loginfo("soldan saga donus basladı")
                        detection_control.publish(True)
                        steering_pub.publish(40)
                        distance_temp = distance
                        while distance - distance_temp < 280:
                            print(distance - distance_temp)
                        steering_pub.publish(0)
                        motor_pub.publish(0)

                detection_control.publish(False)

            if detected_sign_number == 19: #kavsak icin gps bilgisi kullanarak giris yerine göre döndüren algoritma
                rospy.loginfo("kavsak donusu basladı")
                if kavsak_girisi == 1:
                    if current_lane == 1:
                        steering_pub.publish(0)
                        detection_control.publish(True)
                        distance_temp = distance
                        while distance - distance_temp < 450:
                            pass
                        steering_pub.publish(36)
                        distance_temp = distance
                        while distance - distance_temp < 250:  
                            pass
                        steering_pub.publish(-16)
                        distance_temp = distance
                        while distance - distance_temp < 1200:  
                            pass
                        steering_pub.publish(24.28)
                        distance_temp = distance
                        while distance - distance_temp < 350:  
                            pass
                    else:
                        steering_pub.publish(0)
                        detection_control.publish(True)
                        distance_temp = distance
                        while distance - distance_temp < 450:
                            pass
                        steering_pub.publish(36)
                        distance_temp = distance
                        while distance - distance_temp < 300: 
                            pass
                        steering_pub.publish(16)
                        distance_temp = distance
                        while distance - distance_temp < 100: 
                            pass
                        steering_pub.publish(-16)
                        distance_temp = distance
                        while distance - distance_temp < 1250:  
                            pass
                        steering_pub.publish(12)
                        distance_temp = distance
                        while distance - distance_temp < 300:  
                            pass
                elif kavsak_girisi == 2: #distance ile
                    if current_lane == 1:
                        steering_pub.publish(0)
                        detection_control.publish(True)
                        distance_temp = distance
                        while distance - distance_temp < 450:
                            pass
                        steering_pub.publish(36)
                        distance_temp = distance
                        while distance - distance_temp < 300:  
                            pass
                        steering_pub.publish(-20)
                        distance_temp = distance
                        while distance - distance_temp < 500:  
                            pass
                        steering_pub.publish(20.28)
                        distance_temp = distance
                        while distance - distance_temp < 360:  
                            pass
                    else:
                        steering_pub.publish(0)
                        detection_control.publish(True)
                        distance_temp = distance
                        while distance - distance_temp < 450:
                            pass
                        steering_pub.publish(36)
                        distance_temp = distance
                        while distance - distance_temp < 360: 
                            pass
                        steering_pub.publish(-20)
                        distance_temp = distance
                        while distance - distance_temp < 550:  
                            pass
                        steering_pub.publish(20)
                        distance_temp = distance
                        while distance - distance_temp < 360:  
                            pass
                elif kavsak_girisi == 3:
                    if current_lane == 1:
                        steering_pub.publish(0)
                        detection_control.publish(True)
                        distance_temp = distance
                        while distance - distance_temp < 450:
                            pass
                        steering_pub.publish(-36)
                        distance_temp = distance
                        while distance - distance_temp < 250:  
                            pass
                        steering_pub.publish(-16)
                        distance_temp = distance
                        while distance - distance_temp < 1200:  
                            pass
                        steering_pub.publish(24.28)
                        distance_temp = distance
                        while distance - distance_temp < 350:  
                            pass
                    else:
                        steering_pub.publish(0)
                        detection_control.publish(True)
                        distance_temp = distance
                        while distance - distance_temp < 450:
                            pass
                        steering_pub.publish(36)
                        distance_temp = distance
                        while distance - distance_temp < 300: 
                            pass
                        steering_pub.publish(16)
                        distance_temp = distance
                        while distance - distance_temp < 100: 
                            pass
                        steering_pub.publish(-16)
                        distance_temp = distance
                        while distance - distance_temp < 1280:  
                            pass
                        steering_pub.publish(12)
                        distance_temp = distance
                        while distance - distance_temp < 300:  
                            pass
                elif kavsak_girisi == 4:
                    if current_lane == 1:
                        steering_pub.publish(0)
                        detection_control.publish(True)
                        distance_temp = distance
                        while distance - distance_temp < 450:
                            pass
                        steering_pub.publish(36)
                        distance_temp = distance
                        while distance - distance_temp < 250:  
                            pass
                        steering_pub.publish(-16)
                        distance_temp = distance
                        while distance - distance_temp < 120:  
                            pass
                        steering_pub.publish(24.28)
                        distance_temp = distance
                        while distance - distance_temp < 350:  
                            pass
                    else:
                        steering_pub.publish(0)
                        detection_control.publish(True)
                        distance_temp = distance
                        while distance - distance_temp < 450:
                            pass
                        steering_pub.publish(36)
                        distance_temp = distance
                        while distance - distance_temp < 300: 
                            pass
                        steering_pub.publish(16)
                        distance_temp = distance
                        while distance - distance_temp < 100: 
                            pass
                        steering_pub.publish(-16)
                        distance_temp = distance
                        while distance - distance_temp < 1280:  
                            pass
                        steering_pub.publish(12)
                        distance_temp = distance
                        while distance - distance_temp < 300:  
                            pass
                detection_control.publish(False) 
