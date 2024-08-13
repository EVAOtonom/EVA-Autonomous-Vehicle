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
            (40.789775, 29.509026),  # sol alt
            (40.789819, 29.508973),  # sağ alt
            (40.789775, 29.508908),  # sağ üst
            (40.789726, 29.508954)   # sol üst
        ],
        2: [
            (40.789781, 29.509203),  # sol alt
            (40.789825, 29.509142),  # sağ alt
            (40.789736, 29.509139),  # sol üst
            (40.789791, 29.509091)   # sağ üst
        ],
        3: [
            (40.789980, 29.509217),  # sağ alt
            (40.789931, 29.509268),  # sol alt
            (40.789872, 29.509171),  # sol üst
            (40.789915, 29.509104)   # sağ üst
        ],
        4: [
            (40.789889, 29.508974),  # sol üst
            (40.789925, 29.509040),  # sol alt
            (40.789999, 29.508946),  # sağ alt
            (40.789962, 29.508899)   # sağ üst
        ]
        5: [
            (40.789887, 29.509510), #sol üst
            (40.789917, 29.509575), #sol alt
            (40.789960, 29.509508), #sağ alt
            (40.789923, 29.509449) #sağ üst
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
