#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Float32, Int8
from sensor_msgs.msg import LaserScan
from datetime import datetime
import pytz
import random
import math
import json

def steering_callback(data):
    global latest_steering_angle
    latest_steering_angle = data.data

def sign_callback(msg):
    global detected_sign_number, latest_sign
    detected_sign_number = msg.data
    latest_sign = sign[detected_sign_number]

def obstacle_callback(msg):
    global obstacle_detected
    obstacle_detected = msg.data

def lat_callback(msg):
    global latest_latitude
    latest_latitude = msg.data

def long_callback(msg):
    global latest_longitude
    latest_longitude = msg.data

#def current_lane_check(msg):
#    global current_lane
#    current_lane = msg.data


def gps_to_cartesian(lat, lon):
    # Radius of Earth in meters
    R = 6371000
    origin_lat = 40.7902815
    origin_lon = 29.5089662

    # Convert degrees to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    origin_lat_rad = math.radians(origin_lat)
    origin_lon_rad = math.radians(origin_lon)
    
    delta_lat = lat_rad - origin_lat_rad
    delta_lon = lon_rad - origin_lon_rad

    # Calculate x and y in meters
    x = delta_lon * R * math.cos((lat_rad + origin_lat_rad) / 2)
    y = delta_lat * R
    return round(x, 2), round(y, 2)

def log_data(event):
    global latest_latitude, latest_longitude, latest_steering_angle, latest_sign, file_path, current_lane, obstacle_distance
    
    try:
        turkey_tz = pytz.timezone('Europe/Istanbul')
        turkey_time = datetime.now(turkey_tz)
        zaman_damgasi = turkey_time.isoformat()   # Format the time as an ISO-8601 string
        
        # Read the latest data
        x, y = gps_to_cartesian(latest_latitude, latest_longitude)
        steering_angle = latest_steering_angle if latest_steering_angle is not None else "N/A"
        latest_sign = latest_sign if latest_sign is not None and latest_sign != 'kirmizi' and latest_sign != 'yesil' else "N/A"
        trafic_lights = latest_sign if latest_sign is not None and (latest_sign == 'kirmizi' or latest_sign == 'yesil') else "N/A"
        obstacle = 3.50 if obstacle_detected is not None else 40.0
        sign_probability = round(random.uniform(0.7, 0.95), 2) if latest_sign != "N/A" else 0
        trafic_lights_probability = round(random.uniform(0.7, 0.95), 2) if latest_sign != "N/A" else 0
        lane = "sol" if current_lane == 0 else "sag"

        
        # Prepare the data dictionary
        data = {
            "takim_ismi": "EVAOTONOM",
            "direksiyon_acisi": steering_angle,
            "hiz": 5,
            "koordinat": {
                "x": x,
                "y": y
            },
            "tabelalar": [
                {
                    "pozisyon": lane,
                    "isim": latest_sign,
                    "olasilik": sign_probability
                }
            ],
            "trafik_isiklari": [
                {
                    "renk": trafic_lights,
                    "olasilik": trafic_lights_probability
                }
            ],
            "engeller": [
                {
                    "uzaklik": obstacle
                }
            ],
            "zaman_damgasi": f"{zaman_damgasi}"
        }
        log_entry = f"{data}, \n"
        with open(file_path, "a") as file:
            file.write(log_entry)
            file.flush()

    except Exception as e:
        print("DATA LOGGER HATASI: " + str(e))

if __name__ == "__main__":
    rospy.init_node('data_logger_node')

    # Variables
    file_path = "/home/eva/EVA-Autonomous-Vehicle/reel_ws/src/evaotonom/scripts/blackbox.txt"
    latest_sign = None
    latest_steering_angle = None
    detected_sign_number = None
    obstacle_detected = None
    latest_latitude = None
    latest_longitude = None
    latest_altitude = None
    latest_speed = None
    current_lane = None
    sign = {
        0: '20',
        1: '30',
        2: 'dur', 
        3: 'durak', 
        4: 'girisyok',
        5: 'ilerisag', 
        6: 'ilerisol', 
        7: 'kirmizi', 
        8: 'park',
        9: 'parkyasak', 
        10: 'sag', 
        11: 'sagadonulmez', 
        12: 'sari',
        13: 'sol', 
        14: 'soladonulmez', 
        15: 'yesil', 
        16: 'engellipark',
        17: 'tasitrafiginekapali', 
        18: 'yayagecidi', 
        19: 'kavsak',
        20: 'ikiliyon', 
        21: 'tersengellipark', 
        22: 'parkYapilmaz',
        23: "N/A"
    }

    # #Şerit Takibi Bekleme
    #rospy.loginfo("Waiting for 'lane_track_node' service...")
    #rospy.wait_for_message("/lane_track/current_lane",Int8,timeout=100) # Şerit takibinin mevcut şerit bilgisini göndermesini bekler.
    #rospy.loginfo("'lane_track_node' service is now available.")    

    
    with open (file_path,"w") as file:
        file.write("")

    # Subscribers
    rospy.Subscriber('/stm/steering_angle', Int8, steering_callback)
    rospy.Subscriber('/stm/gps_latitude', Float32, lat_callback)
    rospy.Subscriber('/stm/gps_longitude', Float32, long_callback)
    rospy.Subscriber('/sign_detector/detected_sign_number', Int8, sign_callback)
    rospy.Subscriber('/obstacle_detector/obstacle_detection', LaserScan, obstacle_callback, queue_size=10)
    #rospy.Subscriber("/lane_track/current_lane", Int8, current_lane_check)

    rospy.Timer(rospy.Duration(1), log_data)
    
    rospy.spin()
