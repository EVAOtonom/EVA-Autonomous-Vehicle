#!/usr/bin/env python3.9
import rospy
import time
import subprocess

def launch_file(package, launch_file):
    subprocess.Popen(["roslaunch", package, launch_file])

def launch_node(package, node_type, node_name):
    subprocess.Popen([
        "gnome-terminal", "--", "bash", "-c", 
        f"source ~/.bashrc; rosrun {package} {node_type} {node_name}; exec bash"
    ])

if __name__ == "__main__":
    
    rospy.init_node("sequence_launcher")
    
    launch_file("rplidar_ros","rplidar_s1.launch")

    time.sleep(5)

    launch_file("zed_wrapper","zed2i.launch")

    time.sleep(5)

    nodes = [
        {"package": "evaotonom", "type": "AKS_Communication.py", "name": "stm32_node"},
        {"package": "evaotonom", "type": "reel-lane-track.py", "name": "lane_track_node"},
        {"package": "evaotonom", "type": "decision_algorithm.py", "name": "decision_node"},
        {"package": "evaotonom", "type": "obstacle_avoidance.py", "name": "obstacle_detector_node"},
        {"package": "evaotonom", "type": "sign_detector.py", "name": "zed_object_detection"},
        {"package": "evaotonom", "type": "gpskavsak.py", "name": "gps_checker"},
    ]

    for node in nodes:
        launch_node(node["package"], node["type"], node["name"])
        time.sleep(2)
