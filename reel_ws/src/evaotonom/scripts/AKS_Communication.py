
# BU KOD YAPAY ZEKA İŞLEMLERİ SONUCUNDA ARACIN KONTROL EDİLEBİLMESİ İÇİN YAZILMIŞTIR.
# gps_latitude, gps_longitude, read_odometer verileri Float32 tipinde yayınlanmaktadır.
# /stm/steering_angle (INT8), /stm/motor_power (INT8), /stm/reset_encoder (Bool), /stm/brake (Bool) topiclerini abone olur ve veri geldiğinde araca iletir. 
# /stm/left_signal, /stm/right_signal topicleri aracın sağa veya sola sinyal lambalarını yakmasını sağlar. BU TOPİC'E GÖNDERDİĞİNİZ SAYI KADAR YANIP SÖNER.

import rospy
from std_msgs.msg import Float32, Bool, Int8
import minimalmodbus
from enum import Enum
import time

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
    DRIVING_OTONOM = 21

class STM_Communication:
    def __init__(self, port, slave_address=1, baudrate=38400):
        self.stm = minimalmodbus.Instrument(port, slave_address)
        self.stm.serial.baudrate = baudrate
        self.gps_latitude = None
        self.gps_latitude_1 = None
        self.gps_latitude_2 = None
        self.gps_longitude = None
        self.gps_longitude_1 = None
        self.gps_longitude_2 = None
        self.read_odometer = None
        self.check_otonom = None

        # Publishers
        self.gps_latitude_pub = rospy.Publisher('/stm/gps_latitude', Float32, queue_size=1)
        self.gps_longitude_pub = rospy.Publisher('/stm/gps_longitude', Float32, queue_size=1)
        self.read_odometer_pub = rospy.Publisher('/stm/read_odometer', Float32, queue_size=1)
        self.check_otonom_pub = rospy.Publisher('/stm/check_otonom', Bool, queue_size=1)
        self.brake_status_pub = rospy.Publisher('/stm/brake_status', Bool, queue_size=1)

        # Subscribers
        rospy.Subscriber('/stm/steering_angle', Int8, self.steering_angle_callback)
        rospy.Subscriber('/stm/motor_power', Int8, self.motor_power_callback)
        rospy.Subscriber('/stm/reset_odometer', Bool, self.reset_odometer_callback)
        rospy.Subscriber('/stm/brake', Bool, self.brake_callback)
        rospy.Subscriber('/stm/left_signal', Int8, self.l_signal_callback)
        rospy.Subscriber('/stm/right_signal', Int8, self.r_signal_callback)

    def send_command(self, num_of_registers, data):
        try:
            datatemp = data
            if -32769 < data < 32768:
                if data < 0:
                    data = 65536 + data
                self.stm.write_register(num_of_registers.value, int(data), functioncode=6)
                rospy.loginfo(f'{num_of_registers.name} degeri {datatemp} olarak gonderildi.')
            else:
                rospy.logwarn("Fonksiyon icerisine 32767 ila -32768 araliginda deger giriniz.")
        except Exception as e:
            rospy.logwarn(f"AKS COMMUNICATION {num_of_registers.name} GONDERME HATASI: {e}")
            pass

    def read_data(self, num_of_registers):
        try:
            data = self.stm.read_register(num_of_registers.value)
            return data
        except Exception as e:
            rospy.logwarn(f"AKS COMMUNICATION {num_of_registers.name} OKUMA HATASI: {e}")
        
    def steering_angle_callback(self, msg):
        try:
            self.send_command(Register.STEERING_ANGLE, msg.data)
        except Exception as e:
            rospy.logwarn(f"AKS COMMUNICATION STEERING ANGLE GONDERME HATASI: {e}")
            return None

    def brake_callback(self, msg):
        try:
            self.send_command(Register.BRAKE, msg.data)
        except Exception as e:
            rospy.logwarn(f"AKS COMMUNICATION BRAKE GONDERME HATASI: {e}")
            return None

    def motor_power_callback(self, msg):
        try:
            self.send_command(Register.MOTOR_POWER, msg.data)
        except Exception as e:
            rospy.logwarn(f"AKS COMMUNICATION MOTOW POWER GONDERME HATASI: {e}")
            return None

    def reset_odometer_callback(self, msg):
        try:
            self.send_command(Register.RESET_ENCODER, msg.data)
        except Exception as e:
            rospy.logwarn(f"AKS COMMUNICATION RESET ENCODER GONDERME HATASI: {e}")
            return None
        
    def right_signal(self, x=5):
        for i in range (0,x):
            self.send_command(Register.RIGHT_TURN_SIGNAL, 1)
            time.sleep(0.8)
            self.send_command(Register.RIGHT_TURN_SIGNAL, 0)
            time.sleep(0.8)
        print("SAG SINYAL BITTI")

    def left_signal(self, x=5):
        for i in range (0,x):
            self.send_command(Register.LEFT_TURN_SIGNAL, 1)
            time.sleep(0.8)
            self.send_command(Register.LEFT_TURN_SIGNAL, 0)
            time.sleep(0.8)
        print("SOL SINYAL BITTI")
    def r_signal_callback(self, msg):
        try:
            self.right_signal(msg.data)
        except Exception as e:
            rospy.logwarn(f"SAG SINYAL GONDERME HATASI: {e}")
            return None
        
    def l_signal_callback(self, msg):
        try:
            self.left_signal(msg.data)
        except Exception as e:
            rospy.logwarn(f"SOL SINYAL GONDERME HATASI: {e}")
            return None
        
    def publish_data(self):
        global pub_rate
        self.gps_latitude_1 = self.read_data(Register.GPS_LATITUDE)
        self.gps_latitude_2 = self.read_data(Register.GPS_LATITUDE_2)
        self.gps_longitude_1 = self.read_data(Register.GPS_LONGITUDE)
        self.gps_longitude_2 = self.read_data(Register.GPS_LONGITUDE_2)
        self.read_odometer = self.read_data(Register.READ_ODOMETER)
        self.check_otonom = self.read_data(Register.DRIVING_OTONOM )
        if self.gps_latitude_1 is not None and self.gps_latitude_2 is not None:
            self.gps_latitude = ((self.gps_latitude_1 * 10000) + self.gps_latitude_2) / 1000000
            self.gps_latitude_pub.publish(self.gps_latitude)
        if self.gps_longitude_1 is not None and self.gps_longitude_2 is not None:
            self.gps_longitude = ((self.gps_longitude_1 * 100000) + (self.gps_longitude_2 * 10)) / 100000000
            self.gps_longitude_pub.publish(self.gps_longitude)
        if self.read_odometer is not None:
            self.read_odometer_pub.publish(self.read_odometer)
        if self.check_otonom is not None:
            self.check_otonom_pub.publish(self.check_otonom)
        pub_rate.sleep()
        
    def spin(self):
        while not rospy.is_shutdown():
            self.publish_data()
            
if __name__ == '__main__':
    try:
        rospy.init_node('stm32_node')
        
        # Veriables
        port = '/dev/ttyUSB0' 
        stm_node = STM_Communication(port,slave_address=1)
        pub_rate = rospy.Rate(1)
        
        stm_node.spin()

    except Exception as e:
        rospy.logwarn(f"AKS COMMUNICATION HATASI: {e}")
        pass    
