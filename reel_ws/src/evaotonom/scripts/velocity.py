#!/usr/bin/env python3.9

import rospy
from std_msgs.msg import Float32, Int8, Bool
from time import time

# Global variables
current_velocity = 0.0
brake_status = False
previous_odom = None
previous_time = None
last_brake_change_time = None
brake_pub = None

# Callback functions
def brake_callback(msg):
    global brake_status, last_brake_change_time
    brake_status = msg.data
    last_brake_change_time = time()  # Update the time when brake status changes

def odometer_callback(msg):
    global previous_odom, previous_time, velocity_pub, current_velocity
    
    current_odom = msg.data  # Incoming data in centimeters
    current_time = time()

    # If first call, update previous values and return
    if previous_odom is None or previous_time is None:
        previous_odom = current_odom
        previous_time = current_time
        return

    # Calculate velocity
    distance_traveled_cm = current_odom - previous_odom # cm
    time_elapsed = current_time - previous_time

    if time_elapsed > 0:
        # cm to meters
        distance_traveled_m = distance_traveled_cm / 100.0

        # m/s to km/h
        velocity_mps = distance_traveled_m / time_elapsed
        velocity_kmh = velocity_mps * 3.6

        # Publish velocity and update current_velocity
        velocity_pub.publish(Float32(velocity_kmh))
        current_velocity = velocity_kmh

    # Update previous values
    previous_odom = current_odom
    previous_time = current_time

    control_motor_power()
    rate.sleep()

def control_motor_power():
    global current_velocity, brake_status, motor_power_pub

    
    if brake_status:
        motor_power_pub.publish(0)
    else:
        if current_velocity > 2.5:
            motor_power_pub.publish(0)
        elif current_velocity < 2.2:
            motor_power_pub.publish(6)

def check_brake_status():
    global last_brake_change_time, brake_pub
    
    if last_brake_change_time is not None and (time() - last_brake_change_time) > 35:
        brake_pub.publish(Bool(False))  
        last_brake_change_time = time()  

if __name__ == '__main__':
    rospy.init_node('stabil_velocity_node')

    # Global variables
    last_brake_change_time = None

    rospy.loginfo("Waiting for 'lane_track_node' service...")
    rospy.loginfo("'lane_track_node' service is now available.")

    # Publishers
    motor_power_pub = rospy.Publisher('/stm/motor_power', Int8, queue_size=1)
    velocity_pub = rospy.Publisher('/vehicle/velocity_kmh', Float32, queue_size=1)
    brake_pub = rospy.Publisher('/stm/brake', Bool, queue_size=1)

    # Subscribers
    rospy.Subscriber('/stm/brake', Bool, brake_callback)
    rospy.Subscriber('/stm/read_odometer', Float32, odometer_callback)

    rate = rospy.Rate(1)  

    rospy.spin()

