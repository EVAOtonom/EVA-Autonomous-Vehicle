#!/usr/bin/env python3.9
# BU KOD YAPAY ZEKA İŞLEMLERİ SONUCUNDA ARACIN KONTROL EDİLEBİLMESİ İÇİN YAZILMIŞTIR.
# gps_latitude, gps_longitude, read_odometer verileri Float32 tipinde yayınlanmaktadır.
# /stm/steering_angle (INT8), /stm/motor_power (INT8), /stm/reset_encoder (Bool), /stm/brake (Bool) topiclerini abone olur ve veri geldiğinde araca iletir. 

import rospy
from std_msgs.msg import Float32, Bool, Int8
import minimalmodbus
from enum import Enum
import threading
import os

class Register(Enum):
    STEERING_ANGLE = 0
    BRAKE = 1
    MOTOR_POWER = 2
    READ_WHEEL_ANGLE = 3
    READ_BRAKE_PRESSED = 4
    READ_BRAKE_RELEASED = 5
    READ_ODOMETER = 6
    REVERSE_COMMAND = 7
    LEFT_TURN_SIGNAL = 8
    RIGHT_TURN_SIGNAL = 9
    EMERGENCY_STOP = 10
    HEADLIGHTS_ON = 11
    MANUAL_DRIVE_MODE = 12
    RESET_ENCODER = 13
    GPS_LATITUDE = 14
    GPS_LATITUDE_2 = 15
    GPS_LONGITUDE = 16
    GPS_LONGITUDE_2 = 17
    GPS_SPEED = 18
    GPS_ALTITUDE = 19
    GPS_IS_LAVID = 20

def send_command(num_of_registers, data): 
    global stm
    try:
        datatemp = data
        if -32769 < data < 32768:
            if data < 0:
                data = 65536 + data
            stm.write_register(num_of_registers.value, int(data), functioncode=6)
            rospy.loginfo(f'{num_of_registers.name} degeri {datatemp} olarak gonderildi.')
        else:
            rospy.logwarn("Fonksiyon icerisine 32767 ila -32768 araliginda deger giriniz.")
    except Exception as e:
        rospy.logwarn(f'{num_of_registers.name} degeri {datatemp} olarak GONDERILEMEDI.')
        rospy.logwarn(f"AKS COMMUNICATION GONDERME HATASI: {e}")
        pass

def read_data(num_of_registers):
    global stm
    try:
        data = stm.read_register(num_of_registers.value)
        return data
    except Exception as e:
        rospy.logwarn(f"AKS COMMUNICATION OKUMA HATASI: {e}")
        return None

def steering_angle_callback(msg):
    try:
        send_command(Register.STEERING_ANGLE, msg.data)
    except Exception as e:
        rospy.logwarn(f"AKS COMMUNICATION STEERING ANGLE GONDERME HATASI: {e}")
        return None

def brake_callback(msg):
    try:
        send_command(Register.BRAKE, msg.data)
    except Exception as e:
        rospy.logwarn(f"AKS COMMUNICATION BRAKE GONDERME HATASI: {e}")
        return None

def motor_power_callback(msg):
    try:
        send_command(Register.MOTOR_POWER, msg.data)
    except Exception as e:
        rospy.logwarn(f"AKS COMMUNICATION MOTOR POWER GONDERME HATASI: {e}")
        return None

def reset_encoder_callback(msg):
    try:
        send_command(Register.RESET_ENCODER, msg.data)
    except Exception as e:
        rospy.logwarn(f"AKS COMMUNICATION RESET ENCODER GONDERME HATASI: {e}")
        return None

def left_signal_callback(msg):
    try:
        send_command(Register.LEFT_TURN_SIGNAL, msg.data)
    except Exception as e:
        rospy.logwarn(f"AKS COMMUNICATION LEFT SIGNAL GONDERME HATASI: {e}")
        return None

def right_signal_callback(msg):
    try:
        send_command(Register.RIGHT_TURN_SIGNAL, msg.data)
    except Exception as e:
        rospy.logwarn(f"AKS COMMUNICATION RIGHT SIGNAL GONDERME HATASI: {e}")
        return None
    
def publish_data():
    global gps_latitude_pub, gps_longitude_pub, read_odometer_pub, gps_latitude, gps_longitude
    rate = rospy.Rate(0.5)  # 2 SANIYEDE 1 KEZ VERI OKUMAYA YARAR
    while not rospy.is_shutdown():
        try:
            gps_latitude_1 = read_data(Register.GPS_LATITUDE)
            gps_latitude_2 = read_data(Register.GPS_LATITUDE_2)
            gps_longitude_1 = read_data(Register.GPS_LONGITUDE)
            gps_longitude_2 = read_data(Register.GPS_LONGITUDE_2)
            read_odometer = read_data(Register.READ_ODOMETER)
            if gps_latitude_1 is not None and gps_latitude_2 is not None:
                gps_latitude = ((gps_latitude_1 * 10000) + gps_latitude_2) / 1000000
                gps_latitude_pub.publish(gps_latitude)
            if gps_longitude_1 is not None and gps_longitude_2 is not None:
                gps_longitude = ((gps_longitude_1 * 100000) + (gps_longitude_2 * 10)) / 100000000
                gps_longitude_pub.publish(gps_longitude)
            if read_odometer is not None:
                read_odometer_pub.publish(read_odometer)
            rate.sleep()
        except Exception as e:
            rospy.logwarn(f" STMPUBLİSH HATASI : {e}")

def handle_subscribers():
    # Subscribers
    rospy.Subscriber('/stm/steering_angle', Int8, steering_angle_callback)
    rospy.Subscriber('/stm/motor_power', Int8, motor_power_callback)
    rospy.Subscriber('/stm/reset_encoder', Bool, reset_encoder_callback)
    rospy.Subscriber('/stm/brake', Bool, brake_callback)
    rospy.Subscriber('/stm/left_signal', Bool, left_signal_callback)
    rospy.Subscriber('/stm/right_signal', Bool, right_signal_callback)
    rospy.spin()  # MESAJ GELDIKCE DONGU CALISIR

if __name__ == '__main__':
    try:
        rospy.init_node('stm32_node')
        os.system("sudo chmod 777 /dev/ttyUSB*") # Butun portlara izin verir
        port = '/dev/ttyUSB0'

        # Veriables
        gps_longitude = 0
        gps_latitude = 0
        stm = minimalmodbus.Instrument(port, slaveaddress=1) # Modbus tanımlaması
        stm.serial.baudrate = 38400

        # Publishers
        gps_latitude_pub = rospy.Publisher('/stm/gps_latitude', Float32, queue_size=10)
        gps_longitude_pub = rospy.Publisher('/stm/gps_longitude', Float32, queue_size=10)
        read_odometer_pub = rospy.Publisher('/stm/read_odometer', Float32, queue_size=10)

        # Aynı anda okuma ve gönderme yapılabilmesi için
        publisher_thread = threading.Thread(target=publish_data)
        subscriber_thread = threading.Thread(target=handle_subscribers)

        publisher_thread.start()
        subscriber_thread.start()

        publisher_thread.join()
        subscriber_thread.join()

    except Exception as e:
        rospy.logwarn(f"AKS COMMUNICATION HATASI: {e}")
        pass