#!/usr/bin/env python3.9

import time
import rospy
from sensor_msgs.msg import Image, PointCloud2
from std_msgs.msg import Int8, Float32MultiArray, Bool, Float32
from cv_bridge import CvBridge
import cv2
from sensor_msgs import point_cloud2
from ultralytics import YOLO
import message_filters
import math
import logging
from evaotonom.msg import Sign
logging.getLogger('ultralytics').setLevel(logging.ERROR)

def obstacle_callback(msg):
    global obstacle_detected
    obstacle_detected = msg.data

def callback(left_image_msg, right_image_msg, point_cloud_msg):
    global depth, last_publish_time, bridge, obstacle_detected, sign_counter, sign_detected, park_counter, not_park_counter
    if obstacle_detected != 1:
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
        left_detections = [] 
        right_detections = []
        sign_detected = False
    
        results_left = model(left_image) # SOL GÖRÜNTÜDEN TESPİT YAPAR
        for result in results_left:
            for box in result.boxes:
                if box.conf > 0.7: 
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    left_class_id = int(box.cls[0])
                    left_detections.append((left_class_id, (x1, y1, x2, y2)))
        
        results_right = model(right_image) # SAG GÖRÜNTÜDEN TESPİT YAPAR
        for result in results_right:
            for box in result.boxes:
                if box.conf > 0.7: 
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    right_class_id = int(box.cls[0])
                    right_detections.append((right_class_id, (x1, y1, x2, y2)))

            for right_result in right_detections: # SOL VE SAG GORUNTUNUN SONUCLARINI BİRBİRİYLE KIYAS ETMEK İCİN
                for left_result in left_detections:
                    class_name_left = class_names[left_result[0]]
                    class_name_right = class_names[right_result[0]]

                    if class_name_left == class_name_right: 
                        if class_name_right == 'park' or class_name_right == 'engellipark': # PARK VE ENGELLİ PARK İCİN DOGRULAMA 
                           sign_counter[class_name_right] += 1
                           if sign_counter[class_name_right] % park_counter == 0:
                                depth = calculate_depth(point_cloud, (right_result[1]), original_width, original_height)
                                if depth is not None and math.isnan(depth) == False and math.isinf(depth) == False and depth != -1:                                                
                                        tabela_bilgi(class_name_right, depth)
                                        x1, y1, x2, y2 = right_result[1]
                                        cv2.rectangle(right_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                                        label = f'{class_name_right} ({depth:.2f}m)' if depth is not None else class_name_right
                                        cv2.putText(right_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                                        print(f"LEVHA: {class_name_right} UZAKLIK: {depth:.2f}m")
                                        sign_detected = True

                        else: # DIGER LEVHALARIN ICIN DOGRULAMA
                            sign_counter[class_name_right] += 1
                            if sign_counter[class_name_right] % not_park_counter == 0:

                                depth = calculate_depth(point_cloud, (right_result[1]), original_width, original_height)
                                if depth is not None and math.isnan(depth) == False and math.isinf(depth) == False and depth != -1:                                                
                                        tabela_bilgi(class_name_right, depth)
                                        x1, y1, x2, y2 = right_result[1]
                                        cv2.rectangle(right_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                                        label = f'{class_name_right} ({depth:.2f}m)' if depth is not None else class_name_right
                                        cv2.putText(right_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                                        print(f"LEVHA: {class_name_right} UZAKLIK: {depth:.2f}m")
                                        sign_detected = True

        if sign_detected == False: # LEVHA ALGILANMADIGI DURUMDA SANIYEDE 1, 23 YAYINLAR
            current_time = time.time()
            if current_time - last_publish_time >= 1.0:
                detected_sign.sign_index = 0
                detected_sign.depth = 0
                sign_pub.publish(detected_sign)
                last_publish_time = current_time
                    
        cv2.imshow("EVA OTONOM LEVHA TESPITI SAG", right_image)
        cv2.waitKey(1)

def calculate_depth(point_cloud, boundingbox, width, height):
    # Scale bounding box coordinates back to the original image size
    x_center = int((boundingbox[0] + boundingbox[2]) / 2 * (width / 416))
    y_center = int((boundingbox[1] + boundingbox[3]) / 2 * (height / 416))

    # Convert PointCloud2 to 3D point using point_cloud2.read_points
    point_gen = point_cloud2.read_points(point_cloud, field_names=("x", "y", "z"), uvs=[[x_center, y_center]])
    point = next(point_gen, None)

    if point is not None and len(point)>0:
        distance = math.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
        if math.isnan(distance) == False and math.isinf(distance) == False and distance is not None:
            return distance
    else:
        return -1
    
def tabela_bilgi(class_name, depth_in_meters):
    global x1, y1, x2, y2, obstacle_detected
    
    if class_name == "kirmizi" and depth_in_meters is not None and depth_in_meters < 9.0:
        detected_sign.sign_index = 7
        detected_sign.depth = depth_in_meters
        sign_pub.publish(detected_sign)

    elif class_name == "yesil" and depth_in_meters is not None and depth_in_meters < 9.0:
        detected_sign.sign_index = 15
        detected_sign.depth = depth_in_meters
        sign_pub.publish(detected_sign)

    if obstacle_detected == 0:  # ENGEL TESPİT EDİLMEDİĞİ DURUMDA ÇALIŞMASI GEREKEN KARAR ALGORİTMALARI
        if class_name == "20" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index= 0
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "30" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 1
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "dur" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 2
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "durak" and depth_in_meters is not None and depth_in_meters < 15.0:
            detected_sign.sign_index = 3
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "girisyok" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 4
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "ilerisag" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 5
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "ilerisol" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 6
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "park" and depth_in_meters is not None and depth_in_meters < 30.0:
            detected_sign.sign_index = 8
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)
            bounding_box = [float(x1), float(y1), float(x2), float(y2), float(416)]
            msg = Float32MultiArray()
            msg.data = bounding_box
            position_pub.publish(msg)

        elif class_name == "parkyasak" and depth_in_meters is not None and depth_in_meters < 9.5:
            detected_sign.sign_index = 9
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "sag" and depth_in_meters is not None and depth_in_meters < 10.0:
            detected_sign.sign_index = 10
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "sagadonulmez" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 11
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "sari" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 12
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "sol" and depth_in_meters is not None and depth_in_meters < 10.0:
            detected_sign.sign_index = 13
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "soladonulmez" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 14
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "engellipark" and depth_in_meters is not None and depth_in_meters < 9.5:
            detected_sign.sign_index = 16
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "tasittrafiginekapali" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 17
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "yayagecidi" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 18
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "kavsak" and depth_in_meters is not None and depth_in_meters < 7.0:
            detected_sign.sign_index = 19
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "ikiliyon" and depth_in_meters is not None and depth_in_meters < 0.01:
            detected_sign.sign_index = 20
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "tersengellipark" and depth_in_meters is not None and depth_in_meters < 9.5:
            detected_sign.sign_index = 21
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

        elif class_name == "parkyapilmaz" and depth_in_meters is not None and depth_in_meters < 9.5:
            detected_sign.sign_index = 22
            detected_sign.depth = depth_in_meters
            sign_pub.publish(detected_sign)

if __name__ == '__main__':
    rospy.init_node('zed_object_detection')

    # Veriables
    model = YOLO('/home/eva/EVA-Autonomous-Vehicle/reel_ws/src/evaotonom/scripts/sol300best.pt')
    bridge = CvBridge()
    left_image = None
    right_image = None
    point_cloud = None
    depth = Float32()      
    obstacle_detected = 0
    x1, y1, x2, y2 = (0,) *4
    left_detected = 0
    class_names = {
            0: '20', 1: '30', 2: 'dur', 3: 'durak', 4: 'girisyok',
            5: 'ilerisag', 6: 'ilerisol', 7: 'kirmizi', 8: 'park',
            9: 'parkyasak', 10: 'sag', 11: 'sagadonulmez', 12: 'sari',
            13: 'sol', 14: 'soladonulmez', 15: 'yesil', 16: 'engellipark',
            17: 'tasitrafiginekapali', 18: 'yayagecidi', 19: 'kavsak',
            20: 'ikiliyon', 21: 'tersengellipark', 22: 'parkyapilmaz'
        }
    park_counter = 10
    not_park_counter = 6
    sign_counter = {
    '20': 0, '30': 0, 'dur': 0, 'durak': 0,
    'girisyok': 0, 'ilerisag': 0, 'ilerisol': 0,'kirmizi': 0,
    'park': 0, 'parkyasak': 0, 'sag': 0, 'sagadonulmez': 0,
    'sari': 0, 'sol': 0, 'soladonulmez': 0, 'yesil': 0,
    'engellipark': 0, 'tasitrafiginekapali': 0, 'yayagecidi': 0,
    'kavsak': 0, 'ikiliyon': 0, 'tersengellipark': 0, 'parkyapilmaz': 0
    }

    last_publish_time = time.time()  
    rate = rospy.Rate(10)
    detected_sign = Sign()
    # Subscribers
    left_image_sub = message_filters.Subscriber("/zed2i/zed_node/left_raw/image_raw_color", Image)
    right_image_sub = message_filters.Subscriber("/zed2i/zed_node/right_raw/image_raw_color", Image)
    point_cloud_sub = message_filters.Subscriber("/zed2i/zed_node/point_cloud/cloud_registered", PointCloud2)

    # Publishers
    obstacle_detected_sub = rospy.Subscriber('/obstacle_detector/obstacle_detection', Bool, obstacle_callback)
    ts = message_filters.TimeSynchronizer([left_image_sub, right_image_sub, point_cloud_sub], 10)
    ts.registerCallback(callback)
    position_pub = rospy.Publisher('/sign_detector/position', Float32MultiArray, queue_size=10)
    sign_pub = rospy.Publisher('/sign_detector/sign_info', Sign, queue_size=10)

    # rospy.loginfo("Waiting for 'lane_track_node' service...")
    # rospy.wait_for_message("/lane_track/current_lane",Int8,timeout=100) # Şerit takibinin mevcut şerit bilgisini göndermesini bekler.
    # rospy.loginfo("'lane_track_node' service is now available.")
    
    while not rospy.is_shutdown():
        rate.sleep()