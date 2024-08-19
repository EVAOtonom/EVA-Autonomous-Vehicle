#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Int8, Bool, Float32MultiArray, Float32
import time
from evaotonom.msg import Sign

#sağa ve sola dönüş değiştirildi diğerleride değiştirilecek
def engel_callback(msg):
    global detected_obstacle
    detected_obstacle = msg.data

def sign_callback(msg):
    global detected_sign_number, sign_depth_dict
    depth = msg.depth
    sign_depth_dict[msg.sign_index] = depth
    detected_sign_number= msg.sign_index

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

def rota_callback(msg):
    global rota
    rota = msg.data    

if __name__ == "__main__":
    rospy.init_node("decision_node")

    #Veriables
    detected_sign_number = None

    distance = 0

    current_lane = None

    x1, y1, x2, y2, size, depth = (None,)*6

    kavsak_girisi = None

    rota = None

    none_sayac = 0
    
    durak_counter = 0

    sign_depth_dict = {i: None for i in range(23)}

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
    rospy.Subscriber("/gpskavsak/rota", Int8, rota_callback,queue_size=1)
    rospy.Subscriber("/engel_var_mi", Bool , engel_callback, queue_size=1)

    #Publishers
    steering_pub = rospy.Publisher("/stm/steering_angle", Int8, queue_size=1)
    brake_pub = rospy.Publisher("/stm/brake", Bool, queue_size=1)
    lane_control = rospy.Publisher("/serit_kapat", Bool, queue_size=1)
    obstacle_control = rospy.Publisher("/engel_kapat", Bool, queue_size=1)
    motor_pub = rospy.Publisher("/stm/motor_power", Int8, queue_size=1)
    reset_odom = rospy.Publisher('/stm/reset_odometer', Bool, queue_size=1)
    left_signal = rospy.Publisher('/stm/left_signal', Int8, queue_size= 1)
    right_signal = rospy.Publisher('/stm/right_signal', Int8, queue_size=1)

    #motor_pub.publish(0)
    lane_control.publish(0)

    while not rospy.is_shutdown():
        if detected_sign_number != None:
            if detected_sign_number == 3: # DURAK KARAR ALGORITMASI
                durak_counter = durak_counter +1
                if durak_counter < 3:
                    if current_lane == 1: # SAG SERITTEYSE
                        rospy.loginfo(" @@@@@@@@@@ SAG SERITTEN DURAGA GIRIS BASLIYOR @@@@@@@@@@@@@ ") 
                        brake_pub.publish(1)
                        time.sleep(2) 
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        durak_depth = sign_depth_dict[3]
                        while distance < durak_depth * 100 - 700 : 
                            pass
                        lane_control.publish(1) # Tekrar aynı karar algoritmasına girilmemesi için kullanılmaktadır.
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(5)
                        time.sleep(0.5)
                        steering_pub.publish(28)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 110: # durak giriş arttı 
                            if detected_obstacle == 1:
                                engel_var = 1
                                break
                        if engel_var == 0:
                            obstacle_control.publish(1)
                            while distance < 200:
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
                            left_signal.publish(5)
                            time.sleep(0.2)
                            steering_pub.publish(-28)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 470: #320den 380e
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            steering_pub.publish(32)
                            time.sleep(2)  
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 270:
                                pass
                        else:
                            pass
                    elif current_lane == 0: # SOL SERITTEYSE
                        # rospy.loginfo(" @@@@@@@@@@ SOL SERITTEN DURAGA GIRIS BASLIYOR @@@@@@@@@@@@@ ")  
                        # obstacle_control.publish(1)
                        # brake_pub.publish(1)
                        # time.sleep(2)
                        # reset_odom.publish(1)
                        # time.sleep(0.5)
                        # brake_pub.publish(0)
                        # durak_depth = sign_depth_dict[3]
                        # while distance < int(durak_depth) * 100 - 1000 : 
                        #     pass
                        # lane_control.publish(1)
                        # brake_pub.publish(1)
                        # time.sleep(2)
                        # right_signal.publish(5)
                        # time.sleep(0.2)
                        # reset_odom.publish(1)
                        # time.sleep(0.5)
                        # steering_pub.publish(25)
                        # time.sleep(2)
                        # brake_pub.publish(0)
                        # while distance < 500:  
                        #     pass
                        # reset_odom.publish(1)
                        # time.sleep(0.5)
                        # steering_pub.publish(-30)
                        # time.sleep(2)
                        # while distance < 350:
                        #     pass
                        # brake_pub.publish(1)
                        # time.sleep(2)
                        # steering_pub.publish(0)
                        # time.sleep(10)
                        # left_signal.publish(5)
                        # time.sleep(0.2)
                        # steering_pub.publish(-28)
                        # time.sleep(2)
                        # reset_odom.publish(1)
                        # time.sleep(0.5)
                        # brake_pub.publish(0)
                        # time.sleep(2)
                        # while distance < 400:
                        #     pass
                        # brake_pub.publish(1)
                        # time.sleep(2)
                        # steering_pub.publish(32)
                        # time.sleep(2)  
                        # reset_odom.publish(1)
                        # time.sleep(0.5)
                        # brake_pub.publish(0)
                        # time.sleep(2)
                        # while distance < 270:
                        #     pass
                        rospy.loginfo(" @@@@@@@@@@ SOL SERITTEN DURAGA GIRIS BASLIYOR @@@@@@@@@@@@@ ")  
                        obstacle_control.publish(1)
                        lane_control.publish(1) # Tekrar aynı karar algoritmasına girilmemesi için kullanılmaktadır.
                        brake_pub.publish(1)
                        time.sleep(2) 
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(5)
                        time.sleep(0.2)
                        steering_pub.publish(28)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 310: 
                            pass
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-40)
                        time.sleep(2)
                        while distance < 300: # sag seride gecti
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(5)
                        time.sleep(0.5)
                        steering_pub.publish(28)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 110: # durak giriş arttı 
                            if detected_obstacle == 1:
                                engel_var = 1
                                break
                        if engel_var == 0:
                            obstacle_control.publish(1)
                            while distance < 200:
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
                            left_signal.publish(5)
                            time.sleep(0.2)
                            steering_pub.publish(-28)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 470: #320den 380e
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            steering_pub.publish(32)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 270:
                                pass
                    obstacle_control.publish(0)      
                    lane_control.publish(0) # Tekrar aynı karar algoritmasına girilmemesi için kullanılmaktadır.
                else:
                    pass

            elif detected_sign_number == 2: # DUR
                lane_control.publish(1)
                time.sleep(1)
                brake_pub.publish(1)
                time.sleep(6)
                brake_pub.publish(0)
                time.sleep(2)
                lane_control.publish(0)

            elif detected_sign_number == 15: # YEŞİL IŞIK elif detected_sign_number == 23 çıkarıldı
                brake_pub.publish(0)
                time.sleep(2)

            elif detected_sign_number == 7: # KIRMIZI IŞIK
                brake_pub.publish(1)
                time.sleep(2)


            elif detected_sign_number == 8: # PARK LEVHASINA GORE YAY YAPAR
                lane_control.publish(1)
                obstacle_control.publish(1)
                if sign_depth_dict[8] is not None:
                    #os.system("rosnode kill "+ "lane_track_node")
                    #os.system("rosnode kill "+ "obstacle_detector_node")
                    while sign_depth_dict[8] > 9.0 :
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
                        steering_angle = aci * -50/346
                        print("yay")
                        steering_pub.publish(int(steering_angle))
                        none_sayac = 0
                        time.sleep(0.50)
                    while sign_depth_dict[8] > 3.37:
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
                    detected_sign_number = 1
                    rospy.loginfo("Park edildi")
                else:
                    print("depth is none")
                    
            if detected_sign_number == 20: #ikili yön
                if current_lane ==0: #sol şeritteyse
                    lane_control.publish(1)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    right_signal.publish(4)
                    time.sleep(0.2)                    
                    steering_pub.publish(28)
                    time.sleep(2)
                    while distance < 310:
                        pass
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    steering_pub.publish(-40)
                    time.sleep(2)
                    while distance < 300:
                        pass                    
                    steering_pub.publish(0)
                    time.sleep(2)
                    lane_control.publish(0)
                elif current_lane ==1: #sağ şeritteyse
                    pass
                
            if detected_sign_number == 13: # sola dönüş
                if current_lane == 1: # sag seritten
                    rospy.loginfo("sagdan sola donus basladı")
                    obstacle_control.publish(1)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    left_signal.publish(6)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    left_depth = sign_depth_dict[13]
                    while distance < left_depth*100 - 200:
                        pass
                    lane_control.publish(1)
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
                    while distance < 500:
                        pass
                    steering_pub.publish(0)
                    time.sleep(2)


                elif current_lane == 0: # sol seritten
                    rospy.loginfo("soldan sola donus basladı")
                    obstacle_control.publish(1)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    left_signal.publish(6)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    left_depth = sign_depth_dict[13]
                    while distance < left_depth*100-50:
                        pass
                    lane_control.publish(1)
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
                    obstacle_control.publish(1)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    right_signal.publish(6)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    right_depth = sign_depth_dict[13]
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
                    obstacle_control.publish(1)
                    brake_pub.publish(1)
                    time.sleep(2)
                    reset_odom.publish(1)
                    time.sleep(0.5)
                    right_signal.publish(6)
                    time.sleep(0.5)
                    brake_pub.publish(0)
                    time.sleep(2)
                    right_depth = sign_depth_dict[13]
                    while distance < right_depth*100 -200:
                        pass
                    lane_control.publish(1)
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
                    while distance < 500:
                        pass
                    steering_pub.publish(0)
                    time.sleep(2)

                obstacle_control.publish(0)
                lane_control.publish(0)

            if detected_sign_number == 19: #kavsak icin gps bilgisi kullanarak giris yerine gore donduren algoritma
                obstacle_control.publish(1)
                if kavsak_girisi == 1:
                    rospy.loginfo("@@@@@@@@@kavsak donusu basladi 1. giris")
                    if current_lane == 1:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = sign_depth_dict[19]
                        while distance < kavsak_depth*100 - 250:
                            pass
                        lane_control.publish(1)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(6)
                        time.sleep(0.5)
                        steering_pub.publish(0)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:
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
                        while distance < 1180:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(6)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 320:
                            pass
                    else:
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = sign_depth_dict[19]
                        while distance < kavsak_depth*100 - 500:
                            pass
                        lane_control.publish(1)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(6)
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
                        while distance < 1180:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(6)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:
                            pass
                    brake_pub.publish(0)
                    lane_control.publish(False)
                    obstacle_control.publish(False)

                elif kavsak_girisi == 2: ###################durak sayaci ekli
                    rospy.loginfo(f"@@@@@@@@@kavsak donusu basladi 2. giris duraga {durak_counter} defa girildi")
                    if durak_counter == 2:  
                        if current_lane == 1:
                            rospy.loginfo("@@@@@@@@@kavsak donusu basladi 2. giris sag serit ")
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            brake_pub.publish(0)
                            time.sleep(2)
                            kavsak_depth = sign_depth_dict[19]
                            while distance < kavsak_depth*100 - 250:
                                pass
                            lane_control.publish(1)
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
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
                            while distance < 280:
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
                            right_signal.publish(6)
                            time.sleep(0.5)
                            steering_pub.publish(25)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 300:
                                pass
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            left_signal.publish(4)
                            time.sleep(0.2)                    
                            steering_pub.publish(-28)
                            time.sleep(2)
                            while distance < 310:
                                pass
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            steering_pub.publish(40)
                            time.sleep(2)
                            while distance < 300:
                                pass                    
                            steering_pub.publish(0)
                            time.sleep(2)
                            lane_control.publish(0)
                        else:
                            rospy.loginfo("@@@@@@@@@kavsak donusu basladi 2. giris sol serit ")
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            brake_pub.publish(0)
                            time.sleep(2)
                            kavsak_depth = sign_depth_dict[19]
                            while distance < kavsak_depth*100 - 350:
                                pass
                            lane_control.publish(1)
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
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
                            while distance < 380:
                                pass

                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            steering_pub.publish(-20)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 450:
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
                            time.sleep(0.5)
                            steering_pub.publish(20)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 300:
                                pass

                        brake_pub.publish(0)
                        lane_control.publish(False)
                        obstacle_control.publish(False)
                        
                    elif durak_counter == 1:
                        if current_lane ==1: #sag seritteyse
                            pass

                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = sign_depth_dict[19]
                        while distance < kavsak_depth*100 - 250:
                            pass
                        lane_control.publish(1)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(6)
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
                        while distance < 330:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-22)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1180:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(6)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:
                            pass

                        else:
                            rospy.loginfo("@@@@@@@@@kavsak donusu basladi 2. giris sol serit durak cikisina ")
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            brake_pub.publish(0)
                            time.sleep(2)
                            kavsak_depth = sign_depth_dict[19]
                            while distance < kavsak_depth*100 - 400:
                                pass
                            lane_control.publish(1)
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
                            time.sleep(0.5)
                            steering_pub.publish(0)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 320:
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            steering_pub.publish(36)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 430:
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            steering_pub.publish(-25)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 1200:
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
                            time.sleep(0.5)
                            steering_pub.publish(16)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 350:
                                pass
                        brake_pub.publish(0)
                        lane_control.publish(False)
                        obstacle_control.publish(False)

                elif kavsak_girisi == 3:
                    rospy.loginfo(f"@@@@@@@@@kavsak donusu basladi 3. giris duraga  {durak_counter} defa girildi")
                    if durak_counter == 2:
                        if current_lane == 1:
                            rospy.loginfo("@@@@@@@@@kavsak donusu basladi 3. giris sag serit ikinci cikis ")
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            brake_pub.publish(0)
                            time.sleep(2)
                            kavsak_depth = sign_depth_dict[19]
                            while distance < kavsak_depth*100 - 250:
                                pass
                            lane_control.publish(1)
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
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
                            while distance < 1118:
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
                            time.sleep(0.5)
                            steering_pub.publish(16)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 350:
                                pass
                        else:
                            rospy.loginfo("@@@@@@@@@kavsak donusu basladi 3. giris sol serit 2. cikisa ")
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            brake_pub.publish(0)
                            time.sleep(2)
                            kavsak_depth = sign_depth_dict[19]
                            while distance < kavsak_depth*100 - 400:
                                pass
                            lane_control.publish(1)
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
                            time.sleep(0.5)
                            steering_pub.publish(0)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 350:
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            steering_pub.publish(36)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 430:
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            steering_pub.publish(-25)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 1200:
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
                            time.sleep(0.5)
                            steering_pub.publish(16)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 350:
                                pass
                        brake_pub.publish(0)
                        lane_control.publish(False)
                        obstacle_control.publish(False)
                    elif durak_counter == 1:
                        if current_lane == 1:
                            rospy.loginfo("@@@@@@@@@kavsak donusu basladi 3. giris sag serit durak cikisina ")
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            brake_pub.publish(0)
                            time.sleep(2)
                            kavsak_depth = sign_depth_dict[19]
                            while distance < kavsak_depth*100 - 250:
                                pass
                            lane_control.publish(1)
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
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
                            while distance < 280:
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
                            right_signal.publish(6)
                            time.sleep(0.5)
                            steering_pub.publish(25)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 200:
                                pass
                        else:
                            rospy.loginfo("@@@@@@@@@kavsak donusu basladi 3. giris sol serit durak cikisina ")
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            brake_pub.publish(0)
                            time.sleep(2)
                            kavsak_depth = sign_depth_dict[19]
                            while distance < kavsak_depth*100 - 350:
                                pass
                            lane_control.publish(1)
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
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
                            while distance < 380:
                                pass

                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            steering_pub.publish(-20)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 450:
                                pass
                            brake_pub.publish(1)
                            time.sleep(2)
                            reset_odom.publish(1)
                            time.sleep(0.5)
                            right_signal.publish(6)
                            time.sleep(0.5)
                            steering_pub.publish(20)
                            time.sleep(2)
                            brake_pub.publish(0)
                            time.sleep(2)
                            while distance < 200:
                                pass
                        brake_pub.publish(0)
                        lane_control.publish(False)
                        obstacle_control.publish(False)

                elif kavsak_girisi == 4:
                    rospy.loginfo("@@@@@@@@@kavsak donusu basladi 4. giris")
                    if current_lane == 1:
                        rospy.loginfo("4. giris sag seritten")
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = sign_depth_dict[19]
                        while distance < kavsak_depth*100 - 250:
                            pass
                        lane_control.publish(1)
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
                        while distance < 370:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        steering_pub.publish(-22)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 1090:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(6)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:
                            pass

                    else:
                        rospy.loginfo("4. giris sol seritten")
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        brake_pub.publish(0)
                        time.sleep(2)
                        kavsak_depth = sign_depth_dict[19]
                        while distance < kavsak_depth*100 - 400:
                            pass
                        lane_control.publish(1)
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(6)
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
                        while distance < 1100:
                            pass
                        brake_pub.publish(1)
                        time.sleep(2)
                        reset_odom.publish(1)
                        time.sleep(0.5)
                        right_signal.publish(6)
                        time.sleep(0.5)
                        steering_pub.publish(16)
                        time.sleep(2)
                        brake_pub.publish(0)
                        time.sleep(2)
                        while distance < 350:
                            pass
                    brake_pub.publish(0)
                    lane_control.publish(False)
                    obstacle_control.publish(False)

                # elif kavsak_girisi == 3:
                #     rospy.loginfo(f"@@@@@@@@@kavsak donusu basladi 3. giris duraga  {durak_counter} defa girildi")
                #     if durak_counter == 2:
                #         if current_lane == 1:
                #             rospy.loginfo("@@@@@@@@@kavsak donusu basladi 3. giris sag serit ikinci cikis ")
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             kavsak_depth = sign_depth_dict[19]
                #             while distance < kavsak_depth*100 - 250:
                #                 pass
                #             lane_control.publish(1)
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             right_signal.publish(6)
                #             time.sleep(0.5)
                #             steering_pub.publish(0)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 250:
                #                 pass
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             steering_pub.publish(36)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 350:
                #                 pass
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             steering_pub.publish(-22)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 1118:
                #                 pass
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             right_signal.publish(6)
                #             time.sleep(0.5)
                #             steering_pub.publish(16)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 350:
                #                 pass
                #         else:
                #             rospy.loginfo("@@@@@@@@@kavsak donusu basladi 3. giris sol serit 2. cikisa ")
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             kavsak_depth = sign_depth_dict[19]
                #             while distance < kavsak_depth*100 - 400:
                #                 pass
                #             lane_control.publish(1)
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             right_signal.publish(6)
                #             time.sleep(0.5)
                #             steering_pub.publish(0)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 350:
                #                 pass
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             steering_pub.publish(36)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 430:
                #                 pass
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             steering_pub.publish(-25)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 1200:
                #                 pass
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             right_signal.publish(6)
                #             time.sleep(0.5)
                #             steering_pub.publish(16)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 350:
                #                 pass
                #         brake_pub.publish(0)
                #         lane_control.publish(False)
                #         obstacle_control.publish(False)
                #     elif durak_counter == 1:
                #         if current_lane == 1:
                #             rospy.loginfo("@@@@@@@@@kavsak donusu basladi 3. giris sag serit durak cikisina ")
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             kavsak_depth = sign_depth_dict[19]
                #             while distance < kavsak_depth*100 - 250:
                #                 pass
                #             lane_control.publish(1)
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             right_signal.publish(6)
                #             time.sleep(0.5)
                #             steering_pub.publish(0)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 300:
                #                 pass
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             steering_pub.publish(36)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 280:
                #                 pass
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             steering_pub.publish(-20)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 350:
                #                 pass
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             right_signal.publish(6)
                #             time.sleep(0.5)
                #             steering_pub.publish(25)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 200:
                #                 pass
                #         else:
                #             rospy.loginfo("@@@@@@@@@kavsak donusu basladi 3. giris sol serit durak cikisina ")
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             kavsak_depth = sign_depth_dict[19]
                #             while distance < kavsak_depth*100 - 350:
                #                 pass
                #             lane_control.publish(1)
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             right_signal.publish(6)
                #             time.sleep(0.5)
                #             steering_pub.publish(0)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 300:
                #                 pass                        
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             steering_pub.publish(36)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 380:
                #                 pass

                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             steering_pub.publish(-20)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 450:
                #                 pass
                #             brake_pub.publish(1)
                #             time.sleep(2)
                #             reset_odom.publish(1)
                #             time.sleep(0.5)
                #             right_signal.publish(6)
                #             time.sleep(0.5)
                #             steering_pub.publish(20)
                #             time.sleep(2)
                #             brake_pub.publish(0)
                #             time.sleep(2)
                #             while distance < 200:
                #                 pass
                #         brake_pub.publish(0)
                #         lane_control.publish(False)
                #         obstacle_control.publish(False)

            
