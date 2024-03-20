#!/usr/bin/env python
import rospy
from sensor_msgs.msg import PointCloud2, Image
from sensor_msgs import point_cloud2
from cv_bridge import CvBridge
import cv2
import numpy as np

class DepthCameraListener:
    def __init__(self):
        rospy.init_node('depth_camera_listener', anonymous=True)
        
        self.bridge = CvBridge()
        self.color_img = None  # Renkli görüntüyü saklamak için değişken ekleyin

        # Nokta bulutu için abone ol
        self.point_cloud_topic = "/camera/depth/points"
        rospy.Subscriber(self.point_cloud_topic, PointCloud2, self.point_cloud_callback)

        # Renkli görüntü için abone ol
        self.color_image_topic = "/camera/color/image_raw"  # Kodunuzu güncelledim
        rospy.Subscriber(self.color_image_topic, Image, self.color_image_callback)

    def point_cloud_callback(self, msg):
        # Nokta bulutunu işle
        gen = point_cloud2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True)
        points = np.array(list(gen))

        if len(points) > 0 and self.color_img is not None:
            # En yakın cismin 3D koordinatlarını al
            closest_point = points[np.argmin(points[:, 2])]

            # En yakın cismin 3D koordinatlarını yazdır
            print("En Yakın Cismin Koordinatları (3D):", closest_point)

            # En yakın cismin 3D koordinatlarını piksel koordinatlarına dönüştür
            pixel_x = int((closest_point[0] / closest_point[2]) * 640)
            pixel_y = int((closest_point[1] / closest_point[2]) * 480)

    def color_image_callback(self, msg):
        # Renkli görüntüyü göster
        self.color_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        cv2.imshow("Color Image", self.color_img)
        cv2.waitKey(1)

if __name__ == '__main__':
    depth_camera_listener = DepthCameraListener()
    rospy.spin()