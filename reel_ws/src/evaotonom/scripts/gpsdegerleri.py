#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Float32


def latitude_callback(msg):
    global latitude
    latitude = msg.data

def longitude_callback(msg):
    global longitude
    longitude = msg.data

if __name__ == "__main__":
    rospy.init_node('gps_coordinates', anonymous=True)

    # Variables
    latitude = None
    longitude = None

    # Subscribers
    rospy.Subscriber('/stm/gps_latitude', Float32, latitude_callback)
    rospy.Subscriber('/stm/gps_longitude', Float32, longitude_callback)

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        if latitude is not None and longitude is not None:
            with open("coordinats.txt", "a") as file:
                file.write(f"({latitude}, {longitude}),\n")

        else:
            rospy.logwarn("GPS Verisi alınamıyor")

        rate.sleep()
