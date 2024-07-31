
# BU KOD YAPAY ZEKA İŞLEMLERİ SONUCUNDA ARACIN KONTROL EDİLEBİLMESİ İÇİN YAZILMIŞTIR.
# gps_latitude, gps_longitude, read_odometer verileri Float32 tipinde yayınlanmaktadır.
# /stm/steering_angle (INT8), /stm/motor_power (INT8), /stm/reset_encoder (Bool), /stm/brake (Bool) topiclerini abone olur ve veri geldiğinde araca iletir. 

import rospy
from std_msgs.msg import Float64, Bool, Int8
import minimalmodbus
from enum import Enum

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

class STM_Communication:
    def __init__(self, port, slave_address=1, baudrate=38400):
        self.stm = minimalmodbus.Instrument(port, slave_address)
        self.stm.serial.baudrate = baudrate

        # Publishers
        self.gps_latitude_pub = rospy.Publisher('/stm/gps_latitude', Float64, queue_size=10)
        self.gps_longitude_pub = rospy.Publisher('/stm/gps_longitude', Float64, queue_size=10)
        self.read_odometer_pub = rospy.Publisher('/stm/read_odometer', Float64, queue_size=10)

        # Subscribers
        rospy.Subscriber('/stm/steering_angle', Int8, self.steering_angle_callback)
        rospy.Subscriber('/stm/motor_power', Int8, self.motor_power_callback)
        rospy.Subscriber('/stm/reset_encoder', Bool, self.reset_encoder_callback)
        rospy.Subscriber('/stm/brake', Bool, self.brake_callback)
        
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
            rospy.logwarn(f"AKS COMMUNICATION GONDERME HATASI: {e}")
            pass

    def read_data(self, num_of_registers):
        try:
            data = self.stm.read_register(num_of_registers.value)
            return data
        except Exception as e:
            rospy.logwarn(f"AKS COMMUNICATION OKUMA HATASI: {e}")
            return None
        
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

    def reset_encoder_callback(self, msg):
        try:
            self.send_command(Register.RESET_ENCODER, msg.data)
        except Exception as e:
            rospy.logwarn(f"AKS COMMUNICATION RESET ENCODER GONDERME HATASI: {e}")
            return None

    def publish_data(self):
        gps_latitude_1 = self.read_data(Register.GPS_LATITUDE)
        gps_latitude_2 = self.read_data(Register.GPS_LATITUDE_2)
        gps_longitude_1 = self.read_data(Register.GPS_LONGITUDE)
        gps_longitude_2 = self.read_data(Register.GPS_LONGITUDE_2)
        read_odometer = self.read_data(Register.READ_ODOMETER)
        gps_latitude = ((gps_latitude_1 * 10000) + gps_latitude_2) / 1000000
        gps_longitude = ((gps_longitude_1 * 100000) + (gps_longitude_2 * 10)) / 100000000
        if gps_latitude is not None:
            self.gps_latitude_pub.publish(gps_latitude)
        if gps_longitude is not None:
            self.gps_longitude_pub.publish(gps_longitude)
        if read_odometer is not None:
            self.read_odometer_pub.publish(read_odometer)

    def spin(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            self.publish_data()
            rate.sleep()
            
if __name__ == '__main__':
    try:
        rospy.init_node('stm32_node')
        
        # Veriables
        port = '/dev/ttyUSB2' 
        stm_node = STM_Communication(port)
        
        stm_node.spin()
    except rospy.ROSInterruptException as e:
        rospy.logwarn(f"AKS COMMUNICATION HATASI: {e}")
        pass    
