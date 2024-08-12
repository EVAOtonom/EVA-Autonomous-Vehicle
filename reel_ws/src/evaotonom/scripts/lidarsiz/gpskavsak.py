#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Float32, Int8

def is_within_area(lat, lon, area): 
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

    # Variables
    latitude = None
    longitude = None
    rect_areas = {
        1: [
            (40.7897849, 29.5090326),  # sol alt
            (40.7898167, 29.5089471),  # sağ alt
            (40.7897664, 29.5089062),  # sağ üst
            (40.7897436, 29.5089515)   # sol üst
        ],
        2: [
            (40.7897900, 29.5091680),  # sol alt
            (40.7898205, 29.5091456),  # sağ alt
            (40.7897530, 29.5091077),  # sol üst
            (40.7897827, 29.5090782)   # sağ üst
        ],
        3: [
            (40.7899446, 29.5091915),  # sağ alt
            (40.7899063, 29.5092250),  # sol alt
            (40.7898903, 29.5091935),  # sol üst
            (40.7899213, 29.5091265)   # sağ üst
        ],
        4: [
            (40.7898964, 29.5089334),  # sol üst
            (40.7899169, 29.5089937),  # sol alt
            (40.7899967, 29.5089199),  # sağ alt
            (40.7899829, 29.5088710)   # sağ üst
        ]
    }

    # Wait for the lane tracking node to be ready
    rospy.loginfo("Waiting for 'lane_track_node' service...")
    rospy.wait_for_message("/lane_track/current_lane", Int8, timeout=100)
    rospy.loginfo("'lane_track_node' service is now available.")

    # Subscribers
    rospy.Subscriber('/stm/gps_latitude', Float32, latitude_callback)
    rospy.Subscriber('/stm/gps_longitude', Float32, longitude_callback)

    # Publishers
    kavsak_noktasi_pub = rospy.Publisher("/sign_detector/roundabout", Int8, queue_size=10)

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        if latitude is not None and longitude is not None:
            found_area = False
            for area_num, rect_area in rect_areas.items():
                if is_within_area(latitude, longitude, rect_area):
                    kavsak_noktasi_pub.publish(area_num)
                    rospy.loginfo(f"Kavşak: {area_num}")
                    found_area = True
                    print(latitude,longitude)
                    break
            if not found_area:
                kavsak_noktasi_pub.publish(0)  # No matching area, publish 0
        else:
            rospy.logwarn("Veri alınamıyor")

        rate.sleep()
