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
    
def lane_callback(msg):
    global current_lane
    current_lane = msg.data

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

    current_lane = None

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
    rospy.Subscriber('/sign_detection/tabela', Int8, sign_callback , queue_size=10)
    rospy.Subscriber('/sign_detection/position', Float32MultiArray,position_callback ,queue_size=10)
    rospy.Subscriber("/sign_detection/roundabout", Int8 , kavsak_callback)

    #Publishers
    steering_pub = rospy.Publisher("/stm/steering_angle", Int8, queue_size=100)
    brake_pub = rospy.Publisher("/stm/brake", Bool, queue_size=100)
    detection_control = rospy.Publisher("/decision_algorithm/detection_control", Bool, queue_size=10)
    motor_pub = rospy.Publisher("/stm/motor_power", Int8, queue_size=100)
    reset_odom = rospy.Publisher('/stm/reset_odometer', Bool, queue_size=10)
    left_signal = rospy.Publisher('/stm/left_signal', Int8, queue_size= 10)
    right_signal = rospy.Publisher('/stm/right_signal', Int8, queue_size=10)

    motor_pub.publish(False)
    detection_control.publish(False)

    while not rospy.is_shutdown():
        if detected_sign_number != None:

            if detected_sign_number == 3: # DURAK KARAR ALGORITMASI
                if current_lane == 1: # SAG SERITTEYSE
                    rospy.loginfo(" @@@@@@@@@@ SAG SERITTEN DURAGA GIRIS BASLIYOR @@@@@@@@@@@@@ ")  
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    while distance < 180:  
                        print(distance)
                    print("dist1 bitti")
                    detection_control.publish(True) # Tekrar aynı karar algoritmasına girilmemesi için kullanılmaktadır.
                    brake_pub.publish(1)
                    time.sleep(2)
                    right_signal.publish(2)
                    time.sleep(4)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(28)
                    time.sleep(2)
                    brake_pub.publish(0)
                    while distance < 300:  
                        print(distance)
                    print("dist2 bitti")
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(-40)
                    time.sleep(2)
                    while distance < 300:
                        print(distance)
                    print("dist3 bitti")
                    brake_pub.publish(1)
                    time.sleep(2)
                    steering_pub.publish(0)
                    time.sleep(10)
                    left_signal.publish(2)
                    time.sleep(4)
                    steering_pub.publish(-28)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 320:
                        print(distance)
                    print("dist4 bitti")
                    brake_pub.publish(1)
                    time.sleep(2)
                    steering_pub.publish(32)
                    time.sleep(2)  
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 250:
                        print(distance)
                    print("dist5 bitti")

                if current_lane == 0:  # SOL SERITTEYSE
                        pass

                detection_control.publish(False) # Tekrar aynı karar algoritmasına girilmemesi için kullanılmaktadır.
                
            elif detected_sign_number == 2: # DUR
                detection_control.publish(True)
                time.sleep(1)
                brake_pub.publish(1)
                time.sleep(6)
                brake_pub.publish(0)
                time.sleep(2)
                detection_control.publish(False)

            elif detected_sign_number == 15: # YEŞİL IŞIK elif detected_sign_number == 23 çıkarıldı
                brake_pub.publish(0)
                time.sleep(2)

            elif detected_sign_number == 7: # KIRMIZI IŞIK
                brake_pub.publish(1)
                time.sleep(2)
                
            elif detected_sign_number == 8: # PARK 
                if depth is not None:
                    #os.system("rosnode kill "+ "lane_track_node")
                    #os.system("rosnode kill "+ "obstacle_detector_node")
                    while depth > 337 :
                        print (depth)
                        if x1 == None or x2 == None or size == None:
                            print("None")
                            continue
                        sign_midpoint = (x1 + x2) / 2 # Tespit edilen Levhanın orta noktası alınır
                        im_midpoint = size / 2 # Görselin orta noktası alınır
                        steering_angle = ((im_midpoint - sign_midpoint + 208)*0.192) - 40 # -208 ile 208 arasında olan değer tekerlek açısı için -40 ile 40 arasına çevrilir
                        steering_pub.publish(steering_angle) 
                    time.sleep(0.1)
                    brake_pub.publish(1)
                    time.sleep(2)
                    detected_sign_number = True
                    rospy.loginfo("Park edildi")
                    detection_control.publish(True)

                    #os.system("rosnode kill "+ "stabil_throttle_node")
                    #os.system("rosnode kill "+ "sign_detector_node")
                    
                    #time.sleep(5)
                
            if detected_sign_number == 13: # sola dönüş
                if current_lane == 1: # sag seritten
                    rospy.loginfo("sagdan sola donus basladı")
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    while distance < 550:
                        print(distance)
                    print("dist bitti")
                    time.sleep(0.5)
                    detection_control.publish(True)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    left_signal.publish(4)
                    time.sleep(0.5)
                    steering_pub.publish(-40)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 300:
                        print(distance)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(0)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)

                
                elif current_lane == 0: # sol seritten
                    rospy.loginfo("soldan sola donus basladı")
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    while distance <650:
                        print(distance)
                    print("dist bitti")
                    time.sleep(0.5)
                    detection_control.publish(True)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    left_signal.publish(4)
                    time.sleep(0.5)
                    steering_pub.publish(-40)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 300:
                        print(distance)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)   
                    time.sleep(0.5) 
                    steering_pub.publish(0)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)
                

                detection_control.publish(False)               

            if detected_sign_number == 10: # saga donus
                if current_lane == 1: # sag seritten
                    rospy.loginfo("sagdan saga donus basladı")
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    while distance <550:
                        print(distance)
                    print("dist bitti")
                    time.sleep(0.5)
                    detection_control.publish(True)                       
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    right_signal.publish(4)
                    time.sleep(0.5)
                    steering_pub.publish(40)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 300:
                        print(distance)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(0)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)

                    
                elif current_lane == 0: # sol seritten
                    rospy.loginfo("soldan saga donus basladı")
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    while distance <650:
                        print(distance)
                    print("dist bitti")
                    time.sleep(0.5)
                    detection_control.publish(True)
                    brake_pub.publish(1)
                    time.sleep(2)
                    right_signal.publish(4)
                    time.sleep(0.5)
                    steering_pub.publish(40)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 300:
                        print(distance)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(0)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)
                    
                detection_control.publish(False)

            if detected_sign_number == 19: #kavsak icin gps bilgisi kullanarak giris yerine göre döndüren algoritma
                rospy.loginfo("kavsak donusu basladı")
                if kavsak_girisi == 1:
                    if current_lane == 1:
                        detection_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(0)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)                                                
                        while distance < 450:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(36)
                        time.sleep(2)                        
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 250:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(-16)
                        time.sleep(2)                        
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1200:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(25)
                        time.sleep(2)                        
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                    else:
                        detection_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(0)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 450:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(36)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300: 
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(16)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)                   
                        while distance < 100: 
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(-16)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1250:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(12)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                elif kavsak_girisi == 2: #distance ile
                    if current_lane == 1:
                        detection_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(0)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 450:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(36)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(-20)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 500:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(20.28)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 360:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        
                    else:
                        detection_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(0)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 450:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(36)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 360: 
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(-20)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 550:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(20)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 360:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                elif kavsak_girisi == 3:
                    if current_lane == 1:
                        detection_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(0)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 450:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(-36)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 250:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(-16)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1200:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(25)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                    else:
                        detection_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(0)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 450:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(36)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300: 
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(16)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 100: 
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(-16)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1280:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(12)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                elif kavsak_girisi == 4:
                    if current_lane == 1:
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(0)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        detection_control.publish(True)
                        while distance < 450:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(36)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 250:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(-16)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 120:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(25)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                    else:
                        detection_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(0)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 450:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(36)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300: 
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(16)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 100: 
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(-16)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1280:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        steering_pub.publish(12)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                detection_control.publish(False) 
