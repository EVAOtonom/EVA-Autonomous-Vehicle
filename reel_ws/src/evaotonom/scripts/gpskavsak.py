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
        (41.05758748779297, 28.819002036743164),
        (41.05753789672852, 28.818994407348633),
        (41.05753789672852, 28.819002036743164),
        (41.05751119384766, 28.81903446166992)
    ]
       # Dikdörtgen alanı belirleyen koordinatlar

    # Subscribers
    rospy.Subscriber('/stm/gps_latitude', Float32, latitude_callback)
    rospy.Subscriber('/stm/gps_longitude', Float32, longitude_callback)

    # Publishers
    kavsak_noktasi_pub = rospy.Publisher("/sign_detector/roundabout", Int8, queue_size=10)

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