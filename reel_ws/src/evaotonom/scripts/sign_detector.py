#!/usr/bin/env python3.9
import time
import rospy
from sensor_msgs.msg import Image, PointCloud2
from std_msgs.msg import Int8, Float32MultiArray, Bool, Float32
from cv_bridge import CvBridge
import cv2
import numpy as np
from sensor_msgs import point_cloud2
from ultralytics import YOLO
import message_filters
import threading
import math
from collections import defaultdict
import logging
import os
logging.getLogger('ultralytics').setLevel(logging.ERROR)

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

#model 
model = YOLO(f'{os.path.dirname(os.path.abspath(__file__))}/sol300best.pt')
bridge = CvBridge()

def callback(left_image_msg, right_image_msg, point_cloud_msg):
    global left_image, right_image, point_cloud, original_height, original_width, sign_detected, x1, x2, y1, y2, current_detections, cumulative_counters, last_publish_time, size, detection_limit,bridge
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

        # Detect objects in left image
        results_left = model(left_image)
        left_detected = False
        detected_boxes = []
        sign_detected = False

        for result in results_left:
            class_name = None
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

                        sign_detected = True     
                        
                        # Calculate the depth using the point cloud
                        depth = calculate_depth(point_cloud, (x1, y1, x2, y2))

                        if depth is not None and math.isnan(depth) == False and math.isinf(depth) == False:
                            
                            if class_name in ["park", "engellipark"] and box.conf > 0.9:  # Doğrulama kontrolü
                                cumulative_counters[class_name] += 1
                                current_detections += 1
                                
                            # Güvenlik önlemi: Anahtarın sözlükte var olduğundan emin olun
                            if class_name not in cumulative_counters:
                                if class_name != "parkyapilmaz" and class_name != "soladonulmez" and class_name != "parkyasak":
                                    cumulative_counters[class_name] = 0

                            if class_name != "parkyapilmaz" and class_name != "soladonulmez" and class_name != "parkyasak":
                                cumulative_counters[class_name] += 1
                                current_detections += 1

                            # Algılama sayısı limitine ulaşıldığında kontrol
                            if current_detections >= detection_limit:
                                # En sık tespit edilen işareti bul
                                class_name = max(cumulative_counters, key=cumulative_counters.get)

                                # En sık tespit edilen sınıfı tabela_bilgi fonksiyonuna gönder
                                tabela_bilgi(class_name, calculate_depth(point_cloud, (x1, y1, x2, y2)))

                                # Sayaçları ve algılama sayısını sıfırla
                                cumulative_counters = {class_name: 0 for class_name in class_names.values()}
                                current_detections = 0
                                
                            # Draw bounding box and label on right image
                            cv2.rectangle(right_image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            label = f'{class_name} ({depth:.2f}m)' if depth is not None else class_name

                            cv2.putText(right_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                            if depth is not None:
                                print(f"LEVHA: {class_name} UZAKLIK: {depth:.2f}m")
                            else:
                                pass
        else:
            # 23 kodunu yayınlamak için zaman kontrolü
            current_time = time.time()
            if current_time - last_publish_time >= 1.0:  # 1 saniyede bir kontrol
                tabela_pub.publish(23)
                last_publish_time = current_time

def calculate_depth(point_cloud, boundingbox):
    if sign_detected == True:

        # Scale bounding box coordinates back to the original image size
        x_center = int((boundingbox[0] + boundingbox[2]) / 2 * (original_width / 416))
        y_center = int((boundingbox[1] + boundingbox[3]) / 2 * (original_height / 416))

        # Convert PointCloud2 to 3D point using point_cloud2.read_points
        point_gen = point_cloud2.read_points(point_cloud, field_names=("x", "y", "z"), uvs=[[x_center, y_center]])
        point = next(point_gen, None)

        if point is not None and len(point)>0:
            distance = math.sqrt(point[0]**2 + point[1]**2 + point[2]**2)
            if point is not  math.isnan(distance) and not  math.isinf(distance):
                return distance
        else:
            return None
        
# Initialize only once
cumulative_counters = defaultdict(int)

def tabela_bilgi(class_name, depth_in_meters):
    global x1, y1, x2, y2, size
    if obstacle_detected == 1:  # ENGEL TESPİT EDİLDİĞİ DURUMDA ÇALIŞMASI GEREKEN KARAR ALGORİTMALARI
        if depth_in_meters is not None:
            # Derinlik bilgisini Float32MultiArray formatında yayınla
            depth_msg = Float32()     
            depth_msg.data = depth_in_meters
            depth_pub.publish(depth_msg)

        if class_name == "kirmizi" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(7)

        elif class_name == "yesil" and depth_in_meters is not None and depth_in_meters < 7.0:
            tabela_pub.publish(15)

    elif obstacle_detected == 0:  # ENGEL TESPİT EDİLMEDİĞİ DURUMDA ÇALIŞMASI GEREKEN KARAR ALGORİTMALARI
        if depth_in_meters is not None:
            # Derinlik bilgisini Float32MultiArray formatında yayınla
            depth_msg = Float32()     
            depth_msg.data = depth_in_meters
            depth_pub.publish(depth_msg)

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

        elif class_name == "park" and depth_in_meters is not None and depth_in_meters < 30.0:
            tabela_pub.publish(8)

            data = [float(x1), float(y1), float(x2), float(y2), float(size), float(depth_in_meters)]

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



if __name__ == '__main__':
    rospy.init_node('zed_object_detection')

    # #Şerit Takibi Bekleme
    rospy.loginfo("Waiting for 'lane_track_node' service...")
    rospy.wait_for_message("/lane_track/current_lane",Int8,timeout=100) # Şerit takibinin mevcut şerit bilgisini göndermesini bekler.
    rospy.loginfo("'lane_track_node' service is now available.")    


    # Subscribers
    left_image_sub = message_filters.Subscriber("/zed2i/zed_node/left_raw/image_raw_color", Image)
    right_image_sub = message_filters.Subscriber("/zed2i/zed_node/right_raw/image_raw_color", Image)
    point_cloud_sub = message_filters.Subscriber("/zed2i/zed_node/point_cloud/cloud_registered", PointCloud2)

    # Publishers
    obstacle_detected_sub = rospy.Subscriber('/obstacle_detector/obstacle_detection', Bool, obstacle_callback)
    decision_control_sub = rospy.Subscriber('/decision_algorithm/detection_control', Bool, decision_callback)
    ts = message_filters.TimeSynchronizer([left_image_sub, right_image_sub, point_cloud_sub], 10)
    ts.registerCallback(callback)
    tabela_pub = rospy.Publisher('/sign_detector/detected_sign_number', Int8, queue_size=10)
    position_pub = rospy.Publisher('/sign_detector/position', Float32MultiArray, queue_size=10)
    depth_pub = rospy.Publisher('/sign_detector/depth', Float32, queue_size=10)

    # rospy.loginfo("Waiting for 'lane_track_node' service...")
    # rospy.wait_for_message("/lane_track/current_lane",Int8,timeout=100) # Şerit takibinin mevcut şerit bilgisini göndermesini bekler.
    # rospy.loginfo("'lane_track_node' service is now available.")
    
    # Veriables
    left_image = None
    right_image = None
    point_cloud = None
    original_height = None
    original_width = None
    camera_info = None
    obstacle_detected = 0
    decision_control = None
    x1, y1, x2, y2 = (0,) *4
    size = 416
    class_names = {
            0: '20', 1: '30', 2: 'dur', 3: 'durak', 4: 'girisyok',
            5: 'ilerisag', 6: 'ilerisol', 7: 'kirmizi', 8: 'park',
            9: 'parkyasak', 10: 'sag', 11: 'sagadonulmez', 12: 'sari',
            13: 'sol', 14: 'soladonulmez', 15: 'yesil', 16: 'engellipark',
            17: 'tasitrafiginekapali', 18: 'yayagecidi', 19: 'kavsak',
            20: 'ikiliyon', 21: 'tersengellipark', 22: 'parkyapilmaz'
        }
    
    cumulative_counters = defaultdict(int)    # Kümülatif sayaçlar
    # Algılama sayısı limiti
    detection_limit = 2 # 2 algılamada bir kontrol edilecek
    current_detections = 0  # Mevcut algılama sayısı
    cumulative_counters = {class_name: 0 for class_name in class_names.values()}  # Her bir sınıf için sayaç
    last_publish_time = time.time()  # İlk zaman
    rate = rospy.Rate(1)

    display_thread = threading.Thread(target=display_images)
    display_thread.start()
    rate.sleep()

