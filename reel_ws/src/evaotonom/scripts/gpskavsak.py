#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Float32, Int8, Bool

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
    birinci_counter = 0
    ikinci_counter = 0
    park_flag = False  # Park için bayrak
    
    rect_areas = {
        1: [
            (40.789775, 29.509026),  # sol alt
            (40.789819, 29.508973),  # sağ alt
            (40.789775, 29.508908),  # sağ üst
            (40.789726, 29.508954)   # sol üst
        ],
        2: [
            (40.789766, 29.509219),  # sol alt
            (40.789825, 29.509142),  # sağ alt
            (40.789719, 29.509155),  # sol üst
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
        ],
###############################################Donus Noktalari#################################################
        6: [
            
            (40.790015, 29.508436),     # sağ alt          
            (40.789948, 29.508517),     # sol alt            
            (40.789888, 29.508434),     # sol üst           
            (40.789947, 29.508372)      # sağ üst
        ],
        7: [
            (40.789602, 29.508868),     # sağ alt
            (40.789559, 29.508809),     # sağ üst         
            (40.789508, 29.508900),     # sol üst
   
            (40.789537, 29.508978)      # sol alt
        ],
        8: [
            (40.789767, 29.509367),     # sol üst
            (40.789845, 29.509463),     # sol alt
            (40.789910, 29.509383),     # sağ alt
            (40.789859, 29.509313)      # sağ üst
        ],

###############################################önemli Noktalar#################################################
        9: [
            (40.790157, 29.509209),     # sağ alt       park nokta 
            (40.790134, 29.509158),     # sağ üst         
            (40.790100, 29.509196),     # sol üst
            (40.790134, 29.509236)      # sol alt
        ]
        # 10: [
        #     (40.789979, 29.509342),     # sağ alt       deneme kavsak
        #     (40.789928, 29.509393),     # sağ üst         
        #     (40.789971, 29.509457),     # sol üst
        #     (40.790020, 29.509388)      # sol alt
        # ]



    }

    # Wait for the lane tracking node to be ready
    rospy.loginfo("Waiting for 'lane_track_node' service...")
    rospy.wait_for_message("/lane_track/current_lane", Int8, timeout=100)
    rospy.loginfo("'lane_track_node' service is now available.")

    # Subscribers
    rospy.Subscriber('/stm/gps_latitude', Float32, latitude_callback)
    rospy.Subscriber('/stm/gps_longitude', Float32, longitude_callback)

    # Publishers
    kavsak_noktasi_pub = rospy.Publisher("/sign_detector/roundabout", Int8, queue_size=1)
    obstacle_control_pub = rospy.Publisher("/engel_kapat", Bool, queue_size=1)
    onemli_nokta_pub = rospy.Publisher("/gpskavsak/rota",Int8, queue_size=1)

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        if latitude is not None and longitude is not None:
            found_area = False
            for area_num, rect_area in rect_areas.items():
                if is_within_area(latitude, longitude, rect_area):

                    if area_num in range(6, 9): 
                        obstacle_control_pub.publish(1)
                        rospy.loginfo("viraj")

                    elif area_num in range(1,6):
                        kavsak_noktasi_pub.publish(area_num)
                        rospy.loginfo(f"Kavşak: {area_num}")
                        found_area = True
                            
                    elif area_num == 9 and not park_flag:  # park işlemi için bayrak kontrolü
                        park_flag = True  # Bir kere yayınlandığında bayrak ayarlanır
                        onemli_nokta_pub.publish(9)
                        rospy.loginfo("Park noktası: 9")
                    #elif area_num == 10:
                        #kavsak_noktasi_pub.publish(area_num)
                        #rospy.loginfo(f"Kavşak: {area_num}")

            if not found_area:
                kavsak_noktasi_pub.publish(0)
                obstacle_control_pub.publish(0)  
        else:
            rospy.logwarn("GPS kavsak verisi alınamıyor")

        rate.sleep()
