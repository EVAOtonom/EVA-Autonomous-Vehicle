#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Float32, Int8
from sensor_msgs.msg import LaserScan
import time

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

def log_data(event):
    global latest_latitude, latest_longitude, latest_altitude, latest_speed, latest_steering_angle, latest_sign, obstacle_detected, file_path
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        # Read the latest data
        latitude = latest_latitude if latest_latitude is not None else "N/A"
        longitude = latest_longitude if latest_longitude is not None else "N/A"
        altitude = latest_altitude if latest_altitude is not None else "N/A"
        speed = latest_speed if latest_speed is not None else "N/A"
        steering_angle = latest_steering_angle if latest_steering_angle is not None else "N/A"
        latest_sign = latest_sign if latest_sign is not None else "N/A"
        obstacle = obstacle_detected if obstacle_detected is not None else "N/A"
        
        # Log entry for the data
        log_entry = f"{timestamp}, Steering Angle: {steering_angle}, GPS: ({latitude}, {longitude}, {altitude}), Sign: {latest_sign}, Obstacle: {obstacle}\n"
        with open(file_path, "a") as file:
            file.write(log_entry)
            file.flush()  # Ensure data is written to the file immediately

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
    
    with open (file_path,"w") as file:
        file.write("")

    # Subscribers
    rospy.Subscriber('/stm/steering_angle', Int8, steering_callback)
    rospy.Subscriber('/stm/gps_latitude', Float32, lat_callback)
    rospy.Subscriber('/stm/gps_longitude', Float32, long_callback)
    rospy.Subscriber('/sign_detector/detected_sign_number', Int8, sign_callback)
    rospy.Subscriber('/scan', LaserScan, obstacle_callback, queue_size=10)

    rospy.Timer(rospy.Duration(1), log_data)
    
    rospy.spin()
