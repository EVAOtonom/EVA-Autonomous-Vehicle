#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Float32, Int8

def is_within_area(lat, lon, area): # Yardımcı fonksiyon: Bir noktanın belirli bir alan içinde olup olmadığını kontrol eder
    min_lat = min(point[0] for point in area)
    max_lat = max(point[0] for point in area)
    min_lon = min(point[1] for point in area)
    max_lon = max(point[1] for point in area)
    return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon

def latitude_callback(msg):
    global latitude
    latitude = msg.data

def longitude_callback(msg):
    global longitude
    longitude = msg.data

if __name__ == "__main__":
    rospy.init_node('gps_checker', anonymous=True)

    # Veriables
    latitude = None
    longitude = None
    rect_area = [
        (41.05751419067383, 28.820289611816406),
        (41.057472229003906, 28.820341110229492),
        (41.057464599609375, 28.82032585144043),
        (41.05746078491211, 28.820268630981445)
    ]
       # Dikdörtgen alanı belirleyen koordinatlar

    # Subscribers
    rospy.Subscriber('/stm/gps_latitude', Float32, latitude_callback)
    rospy.Subscriber('/stm/gps_longitude', Float32, longitude_callback)

    # Publishers
    kavsak_noktasi_pub = rospy.Publisher("/sign_detection/roundabout", Int8, queue_size=10)

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        if latitude is not None and longitude is not None:
            corrected_latitude = latitude 
            corrected_longitude = longitude 
            print(corrected_latitude, corrected_longitude)
            if is_within_area(corrected_latitude, corrected_longitude, rect_area):
                kavsak_noktasi_pub.publish(1)
                rospy.loginfo("Kavşak")
            else:
                kavsak_noktasi_pub.publish(0)  # Kavşak değilse 0 yayınla
        else:
            print("veri alınamıyor")
            
        rate.sleep()