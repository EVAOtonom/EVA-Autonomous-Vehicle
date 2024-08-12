#!/usr/bin/env python3.9

import time
import rospy
import subprocess

def launch_file(package, launch_file):
    subprocess.run(["roslaunch", package, launch_file])

if __name__ == "__main__":
    rospy.init_node("zed_sdk")
    launch_file("zed_wrapper","zed2i.launch")
