#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Float32, Int8


def latitude_callback(msg):
    global latitude
    latitude = msg.data

def longitude_callback(msg):
    global longitude
    longitude = msg.data

if __name__ == "__main__":
    rospy.init_node('gps_coordinates', anonymous=True)

    # #Şerit Takibi Bekleme
    rospy.loginfo("Waiting for 'lane_track_node' service...")
    rospy.wait_for_message("/lane_track/current_lane",Int8,timeout=100) # Şerit takibinin mevcut şerit bilgisini göndermesini bekler.
    rospy.loginfo("'lane_track_node' service is now available.")

    # Variables
    latitude = None
    longitude = None
    file_path = "/home/eva/EVA-Autonomous-Vehicle/reel_ws/src/evaotonom/scripts/kordinatlar.txt"

        
    # Subscribers
    rospy.Subscriber('/stm/gps_latitude', Float32, latitude_callback)
    rospy.Subscriber('/stm/gps_longitude', Float32, longitude_callback)

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        if latitude is not None and longitude is not None:
            with open(file_path, "a") as file:
                file.write(f"({latitude}, {longitude}),\n")

        else:
            rospy.logwarn("GPS Verisi alınamıyor")

        rate.sleep()
