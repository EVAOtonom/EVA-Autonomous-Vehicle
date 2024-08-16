#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Int8, Bool, Float32MultiArray, Float32
import time
from evaotonom.msg import Sign

#sağa ve sola dönüş değiştirildi diğerleride değiştirilecek

def sign_callback(msg):
    global detected_sign_number, depth
    detected_sign_number= msg.sign_index
    depth = msg.depth
    if detected_sign_number = 8:
        park_depth = depth

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
    global x1,x2,y1,y2,size
    if len(msg.data) == 5:
        x1,y1,x2,y2,size = msg.data

if __name__ == "__main__":
    rospy.init_node("decision_node")

    #Veriables
    detected_sign_number = None

    distance = 0

    current_lane = None

    x1, y1, x2, y2, size, depth = (None,)*6

    kavsak_girisi = None
    
    none_sayac = 0

    # #ŞERİT TAKİBİ BEKLEME
    # rospy.loginfo("Waiting for 'lane_track_node' service...")
    # rospy.wait_for_message("/lane_track/current_lane",Int8,timeout=100) # Şerit takibinin mevcut şerit bilgisini göndermesini bekler.
    # rospy.loginfo("'lane_track_node' service is now available.")


    #Subscribers
    rospy.Subscriber("/sign_detector/sign_info", Sign, sign_callback, queue_size=1) 
    rospy.Subscriber('/stm/read_odometer', Float32, read_odometer, queue_size=1)
    rospy.Subscriber('/lane_track/current_lane', Int8, lane_callback, queue_size=1)
    rospy.Subscriber('/sign_detector/position', Float32MultiArray,position_callback ,queue_size=1)
    rospy.Subscriber("/sign_detector/roundabout", Int8 , kavsak_callback, queue_size=1)

    #Publishers
    steering_pub = rospy.Publisher("/stm/steering_angle", Int8, queue_size=1)
    brake_pub = rospy.Publisher("/stm/brake", Bool, queue_size=1)
    lane_control = rospy.Publisher("/decision_algorithm/lane_control", Bool, queue_size=1)
    obstacle_control = rospy.Publisher("/decision_algorithm/obstacle_control", Bool, queue_size=1)
    motor_pub = rospy.Publisher("/stm/motor_power", Int8, queue_size=1)
    reset_odom = rospy.Publisher('/stm/reset_odometer', Bool, queue_size=1)
    left_signal = rospy.Publisher('/stm/left_signal', Int8, queue_size= 1)
    right_signal = rospy.Publisher('/stm/right_signal', Int8, queue_size=1)

    #motor_pub.publish(False)
    lane_control.publish(False)

    while not rospy.is_shutdown():
        if detected_sign_number != None:

            if detected_sign_number == 3: # DURAK KARAR ALGORITMASI
                if current_lane == 1: # SAG SERITTEYSE
                    rospy.loginfo(" @@@@@@@@@@ SAG SERITTEN DURAGA GIRIS BASLIYOR @@@@@@@@@@@@@ ") 
                    obstacle_control.publish(True)
                    brake_pub.publish(1)
                    time.sleep(2) 
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    durak_depth = depth
                    while distance < int(durak_depth) * 100 - 250 : # 8.7 gibi bir değer olabilir
                        pass
                    lane_control.publish(True) # Tekrar aynı karar algoritmasına girilmemesi için kullanılmaktadır.
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    right_signal.publish(2)
                    time.sleep(0.5)
                    steering_pub.publish(28)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 280: # durak giriş azaltıldı  
                        pass
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(-40)
                    time.sleep(2)
                    while distance < 300:
                        pass
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(0)
                    time.sleep(10)
                    left_signal.publish(2)
                    time.sleep(4)
                    steering_pub.publish(-28)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 380: #320den 380e
                        pass
                    brake_pub.publish(1)
                    time.sleep(2)
                    steering_pub.publish(32)
                    time.sleep(2)  
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 250:
                        pass
                elif current_lane == 0: # SOL SERITTEYSE
                    rospy.loginfo(" @@@@@@@@@@ SOL SERITTEN DURAGA GIRIS BASLIYOR @@@@@@@@@@@@@ ")  
                    obstacle_control.publish(True)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(40)
                    time.sleep(2)
                    brake_pub.publish(0)
                    while distance < 280:
                        pass
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(-40)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 150:
                        pass
                    reset_odom.publish(1)
                    time.sleep(0.5) # buradan yukarısı güncellenebilir 
                    durak_depth = depth
                    while distance < int(durak_depth) * 100 - 800 : # 8.7 gibi bir değer olabilir
                        pass
                    lane_control.publish(True)
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
                        pass
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(-40)
                    time.sleep(2)
                    while distance < 300:
                        pass
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
                        pass
                    brake_pub.publish(1)
                    time.sleep(2)
                    steering_pub.publish(32)
                    time.sleep(2)  
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 250:
                        pass
                obstacle_control.publish(False)      
                lane_control.publish(False) # Tekrar aynı karar algoritmasına girilmemesi için kullanılmaktadır.
                
            elif detected_sign_number == 2: # DUR
                lane_control.publish(True)
                time.sleep(1)
                brake_pub.publish(1)
                time.sleep(6)
                brake_pub.publish(0)
                time.sleep(2)
                lane_control.publish(False)

            elif detected_sign_number == 15: # YEŞİL IŞIK elif detected_sign_number == 23 çıkarıldı
                brake_pub.publish(0)
                time.sleep(2)

            elif detected_sign_number == 7: # KIRMIZI IŞIK
                brake_pub.publish(1)
                time.sleep(2)
                
            # elif detected_sign_number == 8: # PARK LEVHASINI ORTALAR
            #     if depth is not None:
            #         #os.system("rosnode kill "+ "lane_track_node")
            #         #os.system("rosnode kill "+ "obstacle_detector_node")
            #         while depth > 3.37:
            #             if x1 == None or x2 == None or size == None:
            #                 print("None")
            #                 continue
            #             sign_midpoint = (x1 + x2) / 2 # Tespit edilen Levhanın orta noktası alınır
            #             im_midpoint = size / 2 # Görselin orta noktası alınır
            #             steering_angle = ((im_midpoint - sign_midpoint + 208)*0.192) - 40 # -208 ile 208 arasında olan değer tekerlek açısı için -40 ile 40 arasına çevrilir
            #             steering_pub.publish((int(steering_angle)) * -1)
            #             print(steering_angle)
            #             time.sleep(0.5)
            #         time.sleep(2)
            #         brake_pub.publish(1)
            #         time.sleep(2)
            #         detected_sign_number = True
            #         rospy.loginfo("Park edildi")
            #         detection_control.publish(True)

            #         #os.system("rosnode kill "+ "stabil_throttle_node")
            #         #os.system("rosnode kill "+ "sign_detector_node")
                    
            #         #time.sleep(5)

            elif detected_sign_number == 8: # PARK LEVHASINA GORE YAY YAPAR
                lane_control.publish(True)
                obstacle_control.publish(True)
                if park_depth is not None:
                    #os.system("rosnode kill "+ "lane_track_node")
                    #os.system("rosnode kill "+ "obstacle_detector_node")
                    while park_depth > 9.0 :
                        #print (depth)
                        if (x1 == None or x2 == None or size == None) and none_sayac == 0:
                            print("None")
                            none_sayac = 1
                            continue
                        sign_midpoint = (x1 + x2) / 2 # Tespit edilen Levhanın orta noktası alınır
                        #im_midpoint = size * 5 / 6 # Görselin orta noktası alınır
                        hedef = size * 5 / 6
                        aci = (hedef - sign_midpoint)
                        if aci < 0:
                            aci *= 3
                        steering_angle = aci * -40/346
                        print("yay")
                        steering_pub.publish(int(steering_angle)) 
                        none_sayac = 0
                        time.sleep(0.50)
                    while park_depth > 3.37:
                        if (x1 == None or x2 == None or size == None) and none_sayac == 0:
                            print("None")
                            none_sayac = 1
                            continue
                        sign_midpoint = (x1 + x2) / 2
                        hedef = size / 2
                        steering_angle = (((hedef - sign_midpoint + 208)*0.192) - 40) * -1
                        print("düz")
                        steering_pub.publish(int(steering_angle)) 
                        none_sayac = 0
                        time.sleep(0.50)
                    #time.sleep(0.1)
                    brake_pub.publish(1)
                    time.sleep(2)
                    detected_sign_number = True
                    rospy.loginfo("Park edildi")
                else:
                    print("depth is none")
                
            if detected_sign_number == 13: # sola dönüş
                if current_lane == 1: # sag seritten
                    rospy.loginfo("sagdan sola donus basladı")
                    obstacle_control.publish(True)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    left_signal.publish(6)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    left_depth = depth
                    while distance < left_depth*100 - 150:
                        pass
                    lane_control.publish(True)
                    time.sleep(0.5)
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
                    while distance < 475:
                        pass
                    steering_pub.publish(0)
                    time.sleep(2)

                
                elif current_lane == 0: # sol seritten
                    rospy.loginfo("soldan sola donus basladı")
                    obstacle_control.publish(True)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    left_signal.publish(6)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    left_depth = depth
                    while distance < left_depth*100-50:
                        pass
                    lane_control.publish(True)
                    print("dist bitti")
                    time.sleep(0.5)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(-40)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 400:
                        pass
                    steering_pub.publish(0)
                    time.sleep(2)

                
                obstacle_control.publish(False)
                lane_control.publish(False)               

            if detected_sign_number == 10: # saga donus
                if current_lane == 1: # sag seritten
                    rospy.loginfo("sagdan saga donus basladı")
                    obstacle_control.publish(True)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    right_signal.publish(6)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    right_depth = depth
                    while distance < right_depth*100 -50:
                        pass
                    lane_control.publish(True)
                    time.sleep(0.5)  
                    brake_pub.publish(1)
                    time.sleep(2)                
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(40)
                    time.sleep(2)
                    brake_pub.publish(0)
                    time.sleep(2)
                    while distance < 400:
                        pass
                    steering_pub.publish(0)


                    
                elif current_lane == 0: # sol seritten
                    rospy.loginfo("soldan saga donus basladı")
                    obstacle_control.publish(True)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    right_signal.publish(6)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    right_depth = depth
                    while distance < right_depth*100 -150:
                        pass
                    lane_control.publish(True)
                    time.sleep(0.5)
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
                    while distance < 400:
                        pass
                    steering_pub.publish(0)
                    time.sleep(2)

                obstacle_control.publish(False)
                lane_control.publish(False)

            if detected_sign_number == 19: #kavsak icin gps bilgisi kullanarak giris yerine göre döndüren algoritma
                obstacle_control.publish(True)
                if kavsak_girisi == 1:
                    rospy.loginfo("@@@@@@@@@kavsak donusu basladı 1. giris")
                    if current_lane == 1:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = depth                                    
                        while distance < kavsak_depth*100 - 250:
                            pass
                        lane_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 250:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(36)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-22)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1050:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                    else:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = depth
                        while distance < kavsak_depth*100 - 500:
                            pass
                        lane_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(36)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 400:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-25)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1150:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                elif kavsak_girisi == 2: #distance ile
                    rospy.loginfo("@@@@@@@@@kavsak donusu basladı 2. giris")
                    if current_lane == 1:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = depth
                        while distance < kavsak_depth*100 - 230:
                            pass
                        lane_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(36)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 250:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-20)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(25)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        lane_control.publish(0)
                        
                    else:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = depth
                        while distance < kavsak_depth*100 - 250:
                            pass
                        lane_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(36)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        
                        while distance < 200: 
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-20)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 500:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(20)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                elif kavsak_girisi == 3:
                    rospy.loginfo("@@@@@@@@@kavsak donusu basladı 3. giris")
                    if current_lane == 1:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = depth
                        while distance < kavsak_depth*100 - 250:
                            pass
                        lane_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 250:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(36)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-22)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1050:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                    else:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = depth
                        while distance < kavsak_depth*100 - 350:
                            pass
                        lane_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 200:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(36)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 230:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-25)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1100:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                elif kavsak_girisi == 4:
                    rospy.loginfo("@@@@@@@@@kavsak donusu basladı 4. giris")
                    if current_lane == 1:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = depth                                    
                        while distance < kavsak_depth*100 - 250:
                            pass
                        lane_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 250:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(36)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-22)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1050:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                    else:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = depth
                        while distance < kavsak_depth*100 - 500:
                            pass
                        lane_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(36)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 400:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-25)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1150:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                elif kavsak_girisi == 5: ################DENEME
                    rospy.loginfo("@@@@@@@@@kavsak donusu basladı 5. giris")
                    if current_lane == 1:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = depth                                    
                        while distance < kavsak_depth*100 - 250:
                            pass
                        lane_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 250:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(36)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-22)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1050:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)                        
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                    else:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = depth
                        while distance < kavsak_depth*100 - 500:
                            pass
                        lane_control.publish(True)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 300:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(36)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 400:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-25)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1150:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:  
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                    brake_pub.publish(0)
                    lane_control.publish(False) 
                    obstacle_control.publish(True)
