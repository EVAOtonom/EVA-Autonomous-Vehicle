import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def jabra(msg):
    try:
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")

        
        cv2.imshow("Camera Image", cv_image) 
        cv2.waitKey(1)  
    except Exception as e:
        print(e)

def main():
    rospy.init_node('image_subscriber') 
    
    rospy.Subscriber("/kamera/camera/image_raw", Image, jabra)

    rospy.spin()

if __name__ == '__main__':
    main()
