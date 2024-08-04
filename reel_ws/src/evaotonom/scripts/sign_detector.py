#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image, PointCloud2, CameraInfo
from std_msgs.msg import Int8, Bool, Float32MultiArray
from cv_bridge import CvBridge
import cv2
import numpy as np
from sensor_msgs import point_cloud2
from ultralytics import YOLO
import message_filters
import threading
import math
import logging

logging.getLogger('ultralytics').setLevel(logging.ERROR)

# YOLO model path
model_path = '/home/ece/Masaüstü/dataset/sol300best.pt'
model = YOLO(model_path)
bridge = CvBridge()

# Global variables
left_image = None
right_image = None
point_cloud = None
original_height = None
original_width = None
camera_info = None
obstacle_detected = 0
decision_control = None

x1, y1, x2, y2, size = (0,) *5

class_names = {
        0: '20', 1: '30', 2: 'dur', 3: 'durak', 4: 'girisyok',
        5: 'ilerisag', 6: 'ilerisol', 7: 'kirmizi', 8: 'park',
        9: 'parkyasak', 10: 'sag', 11: 'sagadonulmez', 12: 'sari',
        13: 'sol', 14: 'soladonulmez', 15: 'yesil', 16: 'engellipark',
        17: 'tasitrafiginekapali', 18: 'yayagecidi', 19: 'kavsak',
        20: 'ikiliyon', 21: 'tersengellipark', 22: 'parkYapilmaz'
    }

def callback(left_image_msg, right_image_msg, point_cloud_msg):
    global left_image, right_image, point_cloud, original_height, original_width
    
    # Convert images
    original_left_image = bridge.imgmsg_to_cv2(left_image_msg, "bgr8")
    original_right_image = bridge.imgmsg_to_cv2(right_image_msg, "bgr8")

    # Store original image dimensions
    original_height, original_width = original_left_image.shape[:2]

    # Resize images to 416x416
    left_image = cv2.resize(original_left_image, (416, 416))
    right_image = cv2.resize(original_right_image, (416, 416))

    # Store point cloud
    point_cloud = point_cloud_msg

    # Detect objects in left image
    results_left = model(left_image)
    left_detected = False
    detected_boxes = []

    for result in results_left:
        for box in result.boxes:
            if box.conf > 0.7:  # Adjust threshold as needed
                # Get box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                class_name = class_names.get(class_id, 'Unknown')

                # Draw bounding box and label on left image
                cv2.rectangle(left_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                label = f'{class_name}'
                cv2.putText(left_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                left_detected = True
                detected_boxes.append((x1, y1, x2, y2, class_name))

    if left_detected:
        # Detect objects in right image
        results_right = model(right_image)
        for result in results_right:
            for box in result.boxes:
                if box.conf > 0.7:  # Adjust threshold as needed
                    # Get box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    class_id = int(box.cls[0])
                    class_name = class_names.get(class_id, 'Unknown')

                    # Calculate the depth using the point cloud
                    depth = calculate_depth(point_cloud, (x1, y1, x2, y2))

                    # Draw bounding box and label on right image
                    cv2.rectangle(right_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    label = f'{class_name} ({depth:.2f}m)' if depth is not None else class_name
                    cv2.putText(right_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    print(f"Detected {class_name} with depth {depth:.2f}m")
                    tabela_bilgi(class_name, depth)

def calculate_depth(point_cloud, boundingbox):
    # Scale bounding box coordinates back to the original image size
    x_center = int((boundingbox[0] + boundingbox[2]) / 2 * (original_width / 416))
    y_center = int((boundingbox[1] + boundingbox[3]) / 2 * (original_height / 416))
        
    # Convert PointCloud2 to 3D point using point_cloud2.read_points
    point_gen = point_cloud2.read_points(point_cloud, field_names=("x", "y", "z"), uvs=[[x_center, y_center]])
    point = next(point_gen, None)
        
    if point is not None:
        distance = math.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
        return distance
    else:
        rospy.logwarn("No depth data available at the bounding box center.")
        tabela_pub.publish(23)

def tabela_bilgi(class_name, depth_in_meters):
    if obstacle_detected == 1:  # ENGEL TESPİT EDİLDİĞİ DURUMDA ÇALIŞMASI GEREKEN KARAR ALGORİTMALARI
        if class_name == "kirmizi" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(7)

        elif class_name == "yesil" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(15)

    elif obstacle_detected == 0:  # ENGEL TESPİT EDİLMEDİĞİ DURUMDA ÇALIŞMASI GEREKEN KARAR ALGORİTMALARI
        
        if class_name == "20" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(0)

        elif class_name == "30" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(1)

        elif class_name == "dur" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(2)

        elif class_name == "durak" and depth_in_meters is not None and depth_in_meters < 15.0:
            tabela_pub.publish(3)

        elif class_name == "girisyok" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(4)

        elif class_name == "ilerisag" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(5)

        elif class_name == "ilerisol" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(6)

        elif class_name == "kirmizi" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(7)

        elif class_name == "park" and depth_in_meters is not None and depth_in_meters < 18.0:
            tabela_pub.publish(8)

            data = [float(x1), float(y1), float(x2), float(y2), float(size[1]), float(depth_in_meters)]

            # Float32MultiArray message
            msg = Float32MultiArray()
            msg.data = data

            # Publish Float32MultiArray message
            position_pub.publish(msg)

        elif class_name == "parkyasak" and depth_in_meters is not None and depth_in_meters < 9.5:
            tabela_pub.publish(9)

        elif class_name == "sag" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(10)

        elif class_name == "sagadonulmez" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(11)

        elif class_name == "sari" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(12)

        elif class_name == "sol" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(13)

        elif class_name == "soladonulmez" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(14)

        elif class_name == "yesil" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(15)

        elif class_name == "engellipark" and depth_in_meters is not None and depth_in_meters < 9.5:
            tabela_pub.publish(16)

        elif class_name == "tasittrafiginekapali" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(17)

        elif class_name == "yayagecidi" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(18)

        elif class_name == "kavsak" and depth_in_meters is not None and depth_in_meters < 4.0:
            tabela_pub.publish(19)

        elif class_name == "ikiliyon" and depth_in_meters is not None and depth_in_meters < 0.01:
            tabela_pub.publish(20)

        elif class_name == "tersengellipark" and depth_in_meters is not None and depth_in_meters < 9.5:
            tabela_pub.publish(21)

        elif class_name == "parkyapilmaz" and depth_in_meters is not None and depth_in_meters < 9.5:
            tabela_pub.publish(22)


def display_images():
    global left_image, right_image
    while not rospy.is_shutdown():
        if left_image is not None and right_image is not None:
            cv2.imshow("EVA OTONOM SOL KAMERA", left_image)
            cv2.imshow("EVA OTONOM SAG KAMERA", right_image)
            cv2.waitKey(1)


def camera_info_callback(msg):
    global camera_info
    camera_info = msg

def obstacle_callback(msg):
    global obstacle_detected
    obstacle_detected = msg.data

def decision_callback(msg):
    global decision_control
    decision_control = msg.data


def listener():
    rospy.init_node('zed_object_detection', anonymous=True)
    
    left_image_sub = message_filters.Subscriber("/zed2i/zed_node/left_raw/image_raw_color", Image)
    right_image_sub = message_filters.Subscriber("/zed2i/zed_node/right_raw/image_raw_color", Image)
    point_cloud_sub = message_filters.Subscriber("/zed2i/zed_node/point_cloud/cloud_registered", PointCloud2)

    obstacle_detected_sub = rospy.Subscriber('/obstacle_detected', Int8, obstacle_callback)
    decision_control_sub = rospy.Subscriber('/decision_control', Int8, decision_callback)

    ts = message_filters.TimeSynchronizer([left_image_sub, right_image_sub, point_cloud_sub], 10)
    ts.registerCallback(callback)
    
    # Publishers
    global tabela_pub, position_pub
    tabela_pub = rospy.Publisher('/tabela', Int8, queue_size=10)
    position_pub = rospy.Publisher('/position', Float32MultiArray, queue_size=10)
    
    # Start image display thread
    display_thread = threading.Thread(target=display_images)
    display_thread.start()
    
    rospy.spin()

if __name__ == '__main__':
    listener()

