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
    deneme_counter = 0
    
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
        ],
        # 5: [
        #     (40.789887, 29.509510), #sol üst
        #     (40.789917, 29.509575), #sol alt
        #     (40.789960, 29.509508), #sağ alt
        #     (40.789923, 29.509449) #sağ üst
        # ],

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

            (40.789738, 29.509163),     # sağ alt       önemli nokta 1    
            (40.789662, 29.509238),     # sol alt            
            (40.789624, 29.509171),     # sol üst           
            (40.789705, 29.509104)      # sağ üst
        ],
        10: [
            (40.790161, 29.509016),     # sağ alt       önemli nokta 2
            (40.790130, 29.508983),     # sağ üst         
            (40.790089, 29.509026),     # sol üst
            (40.790114, 29.509067)      # sol alt
        ],
        11: [
            (40.790178, 29.509346),     # sağ alt       DENEME nokta 
            (40.790154, 29.509383),     # sağ üst         
            (40.790205, 29.509378),     # sol üst
            (40.790178, 29.509405)      # sol alt
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

                    elif area_num == 9: # 2. duraktan sonra
                        if birinci_counter != 1:
                            birinci_counter = birinci_counter + 1
                            onemli_nokta_pub.publish(9)
                        else:
                            pass

                    elif area_num == 10: # 3. durak sonraki ışıklar
                        if birinci_counter != 1:
                            ikinci_counter = birinci_counter + 1
                            onemli_nokta_pub.publish(10)
                        else:
                            pass
                    elif area_num == 11: # park deneme
                        if birinci_counter != 1:
                            deneme_counter = birinci_counter + 1
                            onemli_nokta_pub.publish(11)
                    else:
                        pass

            if not found_area:
                kavsak_noktasi_pub.publish(0)
                obstacle_control_pub.publish(0)   
        else:
            rospy.logwarn("GPS kavsak verisi alınamıyor")

        rate.sleep()
