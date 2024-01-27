#!/usr/bin/env python3.9

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


def camera(device):
    rospy.init_node("camera_publisher", anonymous=True)
    camera_pub = rospy.Publisher("camera_scan", Image, queue_size=1)

    rate = rospy.Rate(5)

    try:
        rospy.loginfo("Camera node is running...")
        rospy.sleep(0.5)
        cap = cv2.VideoCapture(device)
        #cap.set(cv2.CAP_PROP_FPS,60)
        if cap.isOpened == False:
            print("Camera is not working.")
            exit()
        while not rospy.is_shutdown():
            ret, image = cap.read()
            if not ret:
                print("Error: Couldn't read frame.")
                break
            #cv2.imshow("camera",image)
            bridge = CvBridge()
            imgMsg = bridge.cv2_to_imgmsg(image)
            camera_pub.publish(imgMsg)
            rate.sleep()
    except rospy.ROSInterruptException:
        rospy.loginfo("Camera node stopped by user.")
    finally:
        cap.release()
if __name__ == "__main__":
    #/home/otonom/otonom_ws/src/camera/src/f
    camera(0)
