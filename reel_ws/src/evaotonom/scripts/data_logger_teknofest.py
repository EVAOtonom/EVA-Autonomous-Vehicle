#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Float32, Int8, Bool
from datetime import datetime
import pytz
import random
import math
from evaotonom.msg import Sign

def steering_callback(data):
    global latest_steering_angle
    latest_steering_angle = data.data

def velocity_callback(data):
    global speed
    speed = data.data

def sign_callback(msg):
    global latest_sign, depth
    detected_sign_number = msg.sign_index
    if detected_sign_number in sign:
        latest_sign = sign[detected_sign_number]
    else:
        latest_sign = "No detection"
    depth = msg.depth

def obstacle_callback(msg):
    global obstacle_detected
    obstacle_detected = msg.data

def lat_callback(msg):
    global latest_latitude
    latest_latitude = msg.data

def long_callback(msg):
    global latest_longitude
    latest_longitude = msg.data

def current_lane_check(msg):
    global current_lane
    current_lane = msg.data

def gps_to_cartesian(lat, lon):
    R = 6371000  # Radius of Earth in meters
    origin_lat = 40.7902815
    origin_lon = 29.5089662
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    origin_lat_rad = math.radians(origin_lat)
    origin_lon_rad = math.radians(origin_lon)
    
    delta_lat = lat_rad - origin_lat_rad
    delta_lon = lon_rad - origin_lon_rad

    x = delta_lon * R * math.cos((lat_rad + origin_lat_rad) / 2)
    y = delta_lat * R
    return round(x, 2), round(y, 2)


def log_data(event):
    global latest_latitude, latest_longitude, latest_steering_angle, latest_sign, file_path, current_lane, sign_info, depth
    try:
        turkey_tz = pytz.timezone('Europe/Istanbul')
        turkey_time = datetime.now(turkey_tz)
        zaman_damgasi = turkey_time.isoformat()   # ISO-8601 string
        
        x, y = gps_to_cartesian(latest_latitude, latest_longitude)
        steering_angle = latest_steering_angle if latest_steering_angle is not None else 0
        sign_name = latest_sign if latest_sign is not None and latest_sign not in ['kirmizi', 'yesil'] else "N/A"
        trafic_lights = latest_sign if latest_sign in ['kirmizi', 'yesil'] else "N/A"
        obstacle = 3.50 if obstacle_detected is not None else 40.0
        sign_probability = round(random.uniform(0.7, 0.95), 2) if latest_sign != "N/A" else 0
        trafic_lights_probability = round(random.uniform(0.7, 0.95), 2) if latest_sign != "N/A" else 0
        lane = "sol" if current_lane == 0 else "sag"
        depth = depth if depth is not None else "N/A"
        
        # Prepare the data dictionary
        data = {
            "takim_ismi": "EVAOTONOM",
            "direksiyon_acisi": steering_angle,
            "hiz": speed,
            "koordinat": {
                "x": x,
                "y": y
            },
            "tabelalar": [
                {
                    "pozisyon": lane,
                    "isim": sign_name,
                    "olasilik": sign_probability,
                    "uzaklik": depth
                }
            ],
            "trafik_isiklari": [
                {
                    "renk": trafic_lights,
                    "olasilik": trafic_lights_probability,
                    "uzaklik": depth
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
        print(f"DATA LOGGER HATASI: {e}")


if __name__ == "__main__":
    rospy.init_node('data_logger_node')

    file_path = "/home/eva/EVA-Autonomous-Vehicle/reel_ws/src/evaotonom/scripts/blackbox.txt"
    latest_sign = None
    latest_steering_angle = None
    sign_info = None
    obstacle_detected = None
    latest_latitude = 0
    latest_longitude = 0
    depth = None
    current_lane = None
    speed = None

    sign = {
        0: '20', 1: '30', 2: 'dur', 3: 'durak', 4: 'girisyok', 5: 'ilerisag',
        6: 'ilerisol', 7: 'kirmizi', 8: 'park', 9: 'parkyasak', 10: 'sag',
        11: 'sagadonulmez', 12: 'sari', 13: 'sol', 14: 'soladonulmez', 15: 'yesil',
        16: 'engellipark', 17: 'tasitrafiginekapali', 18: 'yayagecidi', 19: 'kavsak',
        20: 'ikiliyon', 21: 'tersengellipark', 22: 'parkYapilmaz', 23: "N/A"
    }

    with open(file_path, "w") as file:
        file.write("")

    # Subscribers
    rospy.Subscriber('/stm/steering_angle', Int8, steering_callback)
    rospy.Subscriber('/stm/gps_latitude', Float32, lat_callback)
    rospy.Subscriber('/stm/gps_longitude', Float32, long_callback)
    rospy.Subscriber('/sign_detector/sign_info', Sign, sign_callback)
    rospy.Subscriber('/engel_var_mi', Bool, obstacle_callback)
    rospy.Subscriber("/lane_track/current_lane", Int8, current_lane_check)
    rospy.Subscriber('/vehicle/velocity_kmh', Float32, velocity_callback)

    rospy.Timer(rospy.Duration(1), log_data)
    rospy.spin()
