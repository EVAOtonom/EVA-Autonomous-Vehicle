#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Float32
from time import time

class VelocityCalculator:
    def __init__(self):
        # Odometre abonesi
        self.odometer_sub = rospy.Subscriber('/stm/read_odometer', Float32, self.odometer_callback)
        # Hız yayıncısı
        self.velocity_pub = rospy.Publisher('/vehicle/velocity_kmh', Float32, queue_size=1)

        # Önceki odometre değeri ve zamanını saklayan değişkenler
        self.previous_odom = None
        self.previous_time = None

    def odometer_callback(self, msg):
        current_odom = msg.data  # Gelen veri cm cinsindendir
        current_time = time()

        # Eğer önceki değerler mevcut değilse (ilk çağrıda) güncelle ve geri dön
        if self.previous_odom is None or self.previous_time is None:
            self.previous_odom = current_odom
            self.previous_time = current_time
            return

        # Hız hesaplama
        distance_traveled_cm = current_odom - self.previous_odom  # Mesafe cm cinsindedir
        time_elapsed = current_time - self.previous_time

        if time_elapsed > 0:
            # Santimetreyi metreye çevirelim
            distance_traveled_m = distance_traveled_cm / 100.0

            # Hızı m/s'den km/h'ye çeviriyoruz
            velocity_mps = distance_traveled_m / time_elapsed
            velocity_kmh = velocity_mps * 3.6
            self.velocity_pub.publish(Float32(velocity_kmh))

        # Önceki odometre ve zaman değerlerini güncelle
        self.previous_odom = current_odom
        self.previous_time = current_time

if __name__ == '__main__':
    rospy.init_node('velocity_calculator_node')
    velocity_calculator = VelocityCalculator()
    rospy.spin()