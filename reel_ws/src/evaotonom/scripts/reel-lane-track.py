#!/usr/bin/env python3.9
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image as ros_Image
from std_msgs.msg import Bool, Int8
from keras.models import load_model
from PIL import Image
import cv2
import math
import numpy as np
import copy
import time

def obstacle_callback(msg):
    global obstacle_detected
    obstacle_detected = msg.data

def decision_callback(msg):
    global sign_detected
    sign_detected = msg.data

def initialize_detection_variables():
    midpoints = {label: (0, 0) for label in ['ensol', 'sol', 'sag', 'ensag']}
    endpoints = {label: {'max': (0, 0), 'min': (0, 0)} for label in ['ensol', 'sol', 'sag', 'ensag']}
    areas = {label: 0 for label in ['ensol', 'sol', 'sag', 'ensag']}
    return midpoints, endpoints, areas

def cvtColor(image):
    if len(np.shape(image)) == 3 and np.shape(image)[-2] == 3:
        return image
    else:
        image = image.convert('RGB')
        return image

def normalize(image):
    image = image / 127.5 - 1
    return image

def resize_image(image, size):
    img_width, img_height = image.size #fotoğraftan boyutları alır
    inp_width, inp_height = size # input edilen boyutları alır
    scale = min(inp_width / img_width, inp_height / img_height) # birbirine oranlar
    new_weight = int(img_width * scale) # orana göre yüksekliği günceller
    new_height = int(img_height * scale) # orana göre genişliği günceller
    image = image.resize((new_weight, new_height), Image.BICUBIC) # görüntüyü günceller
    new_image = Image.new('RGB', size, (128, 128, 128)) # yeni görüntüyü oluşturur
    new_image.paste(image, ((inp_width - new_weight) // 2, (inp_height - new_height) // 2)) # yeni görüntüyü istenilen koordinatlara yapıştırır
    return new_image, new_weight, new_height #çıktı olarak yeni fotoğraf datası ve boyutları sunulur

def segment_image(msg):
    global label_names, labels_color, model
    image = Image.fromarray(cv2.cvtColor(msg, cv2.COLOR_BGR2RGB))
    image = cvtColor(image) #RGB Sorgusu ve doğrulaması yapar / kaldırılabilir
    orj_img = copy.deepcopy(image) 
    orj_img_height = np.array(image).shape[0]
    orj_img_width = np.array(image).shape[1] 

    image_data, new_img_width, new_img_height = resize_image(image, (INPUT_SHAPE[1], INPUT_SHAPE[0])) 
    image_data = normalize(np.array(image_data, np.float32)) # 32 bit float tipine ve numpy dizisine dönüştürür. Ardından modelde çalıştırmak için normalize eder
    image_data = np.expand_dims(image_data, 0) # bir batch haline getirilir

    prediction = model.predict(image_data, verbose=0)[0]
    prediction = prediction[int((INPUT_SHAPE[0] - new_img_height) // 2):int((INPUT_SHAPE[0] - new_img_height) // 2 + new_img_height),
            int((INPUT_SHAPE[1] - new_img_width) // 2):int((INPUT_SHAPE[1] - new_img_width) // 2 + new_img_width)] # model tahminini orjinal görüntüye oranlar
    prediction = cv2.resize(prediction, (orj_img_width, orj_img_height), interpolation=cv2.INTER_LINEAR)
    prediction = prediction.argmax(axis=-1) #her piksel için class olma olasılığı en yüksek hangisiyse onu bulur

    seg_img = np.reshape(np.array(colors, np.uint8)[np.reshape(prediction, [-1])], [orj_img_height, orj_img_width, -1]) #her piksele ait olduğu classa göre renk atanır
    image = Image.fromarray(seg_img) # np dizisini görtüntüye dönüştürür
    image = Image.blend(orj_img, image, 0.7) #görüntü ve numpy dizisini belirlenen oranda karıştırır
    blended_image_array = np.array(image)
    return blended_image_array, prediction

def annotate_image (blended_image_array, prediction):
    midpoints, endpoints, areas = initialize_detection_variables()
    for label in range(1, 5): # 4 class için 4 kere döner, bu sayede her class için görüntüde maskeleme yapılır
        label_name = label_names[label]
        y_coordinates, x_coordinates = np.where(prediction == label)
        if len(y_coordinates) == 0 or len(x_coordinates) == 0: # etikete ait hiç bir piksel yoksa for döngüsünü atlar
            continue
        
        areas[label_name] = len(y_coordinates) # kaç piksel varsa o kadar alan
        midpoints[label_name] = ( int(np.mean(x_coordinates)), int(np.mean(y_coordinates)) ) # her etiketin x ve y'de ortalaması bulunur 
        max_y_idx = np.argmax(y_coordinates) 
        min_y_idx = np.argmin(y_coordinates)
        max_y_point = (x_coordinates[max_y_idx], y_coordinates[max_y_idx]) # y'nin en sonunu
        min_y_point = (x_coordinates[min_y_idx], y_coordinates[min_y_idx]) # y'nin en başını bulur
        endpoints[label_name] = {'max': max_y_point, 'min': min_y_point} # classın y ekseninde ilk ve son noktasını sözlüğe kaydeder

        cv2.circle(blended_image_array, (endpoints[label_name]['max'][0], endpoints[label_name]['max'][1]), 10, labels_color[label_name], -1) #şerit başlangıcına bi nokta
        cv2.putText(blended_image_array, str(label_name),(endpoints[label_name]['max'][0], endpoints[label_name]['max'][1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, labels_color[label_name], 2)
        cv2.circle(blended_image_array, (endpoints[label_name]['min'][0], endpoints[label_name]['min'][1]), 10, labels_color[label_name], -1) #şerit sonuna bi nokta
        cv2.putText(blended_image_array, str(label_name),(endpoints[label_name]['min'][0], endpoints[label_name]['min'][1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, labels_color[label_name], 2)
        cv2.circle(blended_image_array, (midpoints[label_name][0], midpoints[label_name][1]), 10, labels_color[label_name], -1) # şeritlerin orta noktasına bi nokta
        cv2.putText(blended_image_array, f"orta {str(label_name)}",(midpoints[label_name][0], midpoints[label_name][1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, labels_color[label_name], 2)
    return blended_image_array, midpoints, endpoints, areas

def steering_control(image, midpoints, endpoints, areas):
        global current_lane_number
        if areas['sol'] <= 50: # sol şerit pikseli 50'den fazla ise orta noktasını alıyor
            midpoints['sol'] = (0, 0)
        if areas['sag'] <= 50: # sag şerit pikseli 50'den fazla ise orta noktasını alıyor
            midpoints['sag'] = (0, 0)
        #image = image[:, :, ::-1].copy() # renk kanallarını tersine çevirir, muhtemelen başka kütüphanede işlemek için düzenleme işlemidir
        if midpoints['sol'] != (0, 0) and midpoints['sag'] != (0, 0): # şeritlerin orta noktası hesaplanabiliyorsa koşulu
            mid_line_y = (midpoints['sol'][1] + midpoints['sag'][1]) / 2
            mid_line_x = (midpoints['sol'][0] + midpoints['sag'][0]) / 2        
        elif midpoints['sag'] == (0, 0) and midpoints['sol'] != (0, 0): # sagın orta noktası yok solun orta noktası var koşulu
            mid_line_y = midpoints['sol'][1]
            mid_line_x = midpoints['sol'][0] + 150                      # sol şeride 150 ekleyerek sag şeritsiz yolun ortasını buluyor

        elif midpoints['sol'] == (0, 0) and midpoints['sag'] != (0, 0): # solun orta noktası yok sagın orta noktası var koşulu
            mid_line_y = midpoints['sag'][1]
            mid_line_x = midpoints['sag'][0] - 150                     # sag seridin orta noktasından 150 piksel çıkartarak yolun ortasını buluyor
        else:
            cv2.putText(image, 'UCGEN CIZILEMEDI',(15, 40), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
            print("UCGEN CIZILEMEDI")

        image = cv2.line(image, ((int(image.shape[1] / 2))-15, 332),
                        ((int(image.shape[1] / 2))-15, int(mid_line_y)), (0, 255, 0), 2)                       # düz çizgiyi çekiyor
        image = cv2.line(image, ((int(image.shape[1] / 2))-15, 332),
                        (int(mid_line_x)-15, int(mid_line_y)), (0, 255, 0), 2)                                 # çapraz çizgiyi çekiyor
        image = cv2.line(image, ((int(image.shape[1] / 2))-15, int(mid_line_y)),
                        (int(mid_line_x)-15, int(mid_line_y)), (0, 255, 0), 2)                                     # yatay çizgiyi çekiyor
        uzaklik_y = (image.shape[0] - mid_line_y)                                                         # cizgi uzunlugunu bulmaya yarar
        uzaklik_x = (((image.shape[1] / 2)) - mid_line_x) - 15                                            # yolun ortasına aracın uzaklığı
        degree = (180 * math.atan(abs(uzaklik_x / uzaklik_y))) / (3.14)                                 # sapma bir açıya dönüştürülür
        steering = int(degree)                                                          # araç için oranlanmış değer

        if uzaklik_x < 0:                                 #saga döndürür
            steering = -steering
        elif uzaklik_x > 0:                               #sola döndürür
            steering = steering

        steering_pub.publish(steering)

        cv2.putText(image, f"tekerlek acisi: {steering}", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255,255,255), thickness=2)
        cv2.putText(image, f"ucgen aci: {degree}", (15, 55), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255,255,255), thickness=2)
        if areas['ensol'] > areas['ensag']: # Mevcut şerit bilgisini ekrana yazdırır
            cv2.putText(image, 'arac SAG seritte',(15,80),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            current_lane_number = 1
        elif areas ['ensag'] > areas ['ensol']: 
            cv2.putText(image, 'arac SOL seritte',(15,80),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            current_lane_number = 0
        else:
            if current_lane_number == 0:
                cv2.putText(image, 'arac SOL seritte',(15,80),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            elif current_lane_number == 1:
                cv2.putText(image, 'arac SAG seritte',(15,80),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        lane_publisher.publish(current_lane_number)    

        #print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
        cv2.imshow("EVA OTONOM LANE TRACK", image)
        cv2.waitKey(1)

def callback():
    try:
        ret, msg = cam.read()
        image, pr = segment_image(msg)
        image, midpoints, endpoints, areas = annotate_image(image, pr)
        steering_control(image, midpoints, endpoints, areas)
    except Exception as e:
        print("SERIT TAKIBI HATASI: " + str(e))
    
if __name__ == "__main__":
    rospy.init_node('lane_track_node') 

    #Variables
    model = load_model('/home/eva/tumVeriSetiyleSeritTakibiModeli.h5', compile=False)
    colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128)]
    INPUT_SHAPE = [480, 640, 3]  # (Height, Width , Color Format) 
    current_lane_number = None
    obstacle_detected, sign_detected = (False,) *2
    cam = cv2.VideoCapture(2)
    label_names = ['background', 'ensol', 'sol', 'sag', 'ensag']
    labels_color = {
        'ensol': (255, 0, 0),  # Kırmızı
        'sol': (0, 255, 0),    # Yeşil
        'sag': (255, 255, 0),  # Sarı
        'ensag': (0, 0, 255)   # Mavi
    }
    initialize_detection_variables()
    
    #Subscribers
    rospy.Subscriber('/obstacle_detector/obstacle_detection', Bool, obstacle_callback)
    rospy.Subscriber('/decision_algorithm/detection_control', Bool, decision_callback)

    #Publishers
    motor_power_pub = rospy.Publisher('/stm/motor_power', Int8, queue_size=10)
    steering_pub = rospy.Publisher("/stm/steering_angle", Int8, queue_size=10)
    lane_publisher = rospy.Publisher("/lane_track/current_lane", Int8, queue_size=10)
    brake_publisher = rospy.Publisher('/stm/brake', Bool, queue_size=10)

    obstacle_detected = False
    motor_power_pub.publish(1)
    while not rospy.is_shutdown():
        callback()
