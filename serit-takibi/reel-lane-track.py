#!/usr/bin/env python3.9
##  SOL SERIT 0, SAG SERIT 1
import rospy
from keras.models import load_model
from PIL import Image
import cv2
import math
import numpy as np
import copy
import time
#import tensorflow as tf
import AKS_Communication as aks
stm =  aks.STM_Communication("/dev/ttyUSB0")
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

    prediction = model.predict(image_data)[0]
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
    global tooclose, show
    midpoints, endpoints, areas = initialize_detection_variables()
    for label in range(1, 5): # 5 class için 5 kere döner, bu sayede her class için görüntüde maskeleme yapılır
        label_name = label_names[label]
        y_coordinates, x_coordinates = np.where(prediction == label)
        if len(y_coordinates) == 0 or len(x_coordinates) == 0: # etikete ait hiç bir piksel yoksa for döngüsünü atlar
            continue
        area = len(y_coordinates) # Bu döngü sayesinde bir classın 500'den az pikseli varsa atlar noktalama yapmaz
        if area < 400:
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
        cv2.circle(blended_image_array, (midpoints[label_name][0], midpoints[label_name][1]), 10, labels_color[label_name], -1)
        cv2.putText(blended_image_array, f"orta {str(label_name)}",(midpoints[label_name][0], midpoints[label_name][1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, labels_color[label_name], 2)

    distance = abs(midpoints['sol'][1] - midpoints['sag'][1]) # işlem sayesinde orta noktaların y ekseninde uzaklıkları bulunur
    if distance > 100: # iki seritten birinin ortadan kaybolduğu durumu tetikleyen koşul
        tooclose = 1
        cv2.putText(blended_image_array, 'middle points are too close',(15, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

    return blended_image_array, midpoints, endpoints, areas

def steering_control(image, midpoints, endpoints, areas):
        global tooclose, current_lane_number
        if areas['sol'] <= 50: # sol şerit pikseli 50'den fazla ise orta noktasını alıyor
            midpoints['sol'] = (0, 0)
        if areas['sag'] <= 50: # sag şerit pikseli 50'den fazla ise orta noktasını alıyor
            midpoints['sag'] = (0, 0)
        #image = image[:, :, ::-1].copy() # renk kanallarını tersine çevirir, muhtemelen başka kütüphanede işlemek için düzenleme işlemidir
        if midpoints['sol'] != (0, 0) and midpoints['sag'] != (0, 0):
            if tooclose == 1:
                road_mid = (midpoints['sol'][0] + midpoints['sag'][0]) / 2          # iki şeridin ortasını buluyor
                if endpoints['sag']['max'][0] - endpoints['sag']['min'][0] < 0:     # viraj sola doğruysa 
                    mid_line_x = +400 + road_mid                                    # orta x'i 100px sağa kaydırıyor
                    mid_line_y = (midpoints['sol'][1] + midpoints['sag'][1]) / 2    # orta y'yi uzaklığınıda iki şeridin orta noktalarının ortalamasına göre çiziyor
                    print("BURDAYIM11111111")
                if endpoints['sag']['max'][0] - endpoints['sag']['min'][0] > 0:   # viraj sağa doğruysa
                    mid_line_x = -400 + road_mid                                    # orta noktayı 100px sola kaydırıyor
                    mid_line_y = (midpoints['sol'][1] + midpoints['sag'][1]) / 2    # aynı
                    print("BURDAYIM222222222")
                if road_mid > image.shape[1] / 2:
                    mid_line_x = -400 + road_mid
                    mid_line_y = (midpoints['sol'][0] + midpoints['sag'][0]) / 2
                    print("BURDAYIM333333333")
                if road_mid < image.shape[1] / 2:
                    mid_line_x = -400 + road_mid
                    mid_line_y = (midpoints['sol'][0] + midpoints['sag'][0]) / 2
                    print("BURDAYIM4444444444")
            else:
                mid_line_y = (midpoints['sol'][1] + midpoints['sag'][1]) / 2
                mid_line_x = (midpoints['sol'][0] + midpoints['sag'][0]) / 2
                print("BURDAYIM55555555555")
        
        elif midpoints['sag'] == (0, 0) and midpoints['sol'] != (0, 0): # sagın orta noktası yok solun orta noktası var koşulu
            mid_line_y = midpoints['sol'][1]
            mid_line_x = midpoints['sol'][0] + 150                      # sol şeride 400 ekleyerek sag şeritsiz yolun ortasını buluyor
            #cv2.circle(image,( mid_line_x, mid_line_y), 10, (255,255,255), -1) #TEK SERİTLİ YOLDA DENE
            print("BURDAYIM66666666666")

        elif midpoints['sol'] == (0, 0) and midpoints['sag'] != (0, 0): # solun orta noktası yok sagın orta noktası var koşulu
            mid_line_y = midpoints['sag'][1]
            mid_line_x = midpoints['sag'][0] - 150                     # sag seridin orta noktasından 400 piksel çıkartarak yolun ortasını buluyor
            #cv2.circle(image, (mid_line_x, mid_line_y), 10, (255,255,255), -1) #TEK SERİTLİ YOLDA DENE SONUCA PİKSEL SAYISINI 400DEN DEĞİŞTİR
            print("BURDAYIM77777777777")
        else:
            cv2.putText(image, 'UCGEN CIZILEMEDI',(15, 40), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
            print("UCGEN CIZILEMEDI")

        image = cv2.line(image, ((int(image.shape[1] / 2)), 270),
                        ((int(image.shape[1] / 2)), int(mid_line_y)), (0, 255, 0),
                        2)                                                                                  # düz çizgiyi çekiyor
        image = cv2.line(image, ((int(image.shape[1] / 2)), 270),
                        (int(mid_line_x), int(mid_line_y)), (0, 255, 0), 2)                                 # çapraz çizgiyi çekiyor
        image = cv2.line(image, ((int(image.shape[1] / 2)), int(mid_line_y)),
                        (int(mid_line_x), int(mid_line_y)), (0, 255, 0), 2)                                 # yatay çizgiyi çekiyor
        uzaklik_y = (image.shape[0] - mid_line_y)                                                         # cizgi uzunlugunu bulmaya yarar
        uzaklik_x = (((image.shape[1] / 2)) - mid_line_x)                                                 # yolun ortasına aracın uzaklığı
        degree = (180 * math.atan(abs(uzaklik_x / uzaklik_y))) / (3.14)                                 # sapma bir açıya dönüştürülür
        steering_data = int(degree)                                                          # araç için oranlanmış değer

        if uzaklik_x < 0:                                 #saga döndürür
            steering_data = steering_data
        elif uzaklik_x > 0:                               #sola döndürür
            steering_data = -steering_data
        stm.send_command(aks.Register.STEERING_ANGLE,steering_data)
        #steeringdatagonder

        cv2.putText(image, f"tekerlek acisi: {steering_data}", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255,255,255), thickness=2)
        cv2.putText(image, f"ucgen aci: {degree}", (15, 55), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255,255,255), thickness=2)
        if areas['ensol'] > areas['ensag']: # Mevcut şerit bilgisini ekrana yazdırır
            cv2.putText(image, 'arac SAG seritte',(15,80),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            current_lane_number = 1
        elif areas ['ensag'] > areas ['ensol']: 
            cv2.putText(image, 'arac SOL seritte',(15,80),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            current_lane_number = 0
        else:
            cv2.putText(image, 'arac XXX seritte',(15,80),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        tooclose = 0

        #print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
        cv2.imshow("EVA OTONOM LANE TRACK", image)
        cv2.waitKey(1)

def callback():
    try:
        ret, frame = cam.read()
        if ret:
            image, pr = segment_image(frame)
            image, midpoints, endpoints, areas = annotate_image(image, pr)
            steering_control(image, midpoints, endpoints, areas)
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    rospy.init_node('lane_track_node', anonymous=True) 
    model = load_model('/home/eva/tumVeriSetiyleSeritTakibiModeli.h5', compile=False)
    colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128)]
    INPUT_SHAPE = [480, 640, 3]  # (Height, Width , Color Format) 
    current_lane_number = None
    distance = 0
    scan = None
    tooclose = 0
    show = False
    passing_state = 0
    label_names = ['background', 'ensol', 'sol', 'sag', 'ensag']
    labels_color = {
        'ensol': (255, 0, 0),  # Kırmızı
        'sol': (0, 255, 0),    # Yeşil
        'sag': (255, 255, 0),  # Sarı
        'ensag': (0, 0, 255)   # Mavi
    }
    initialize_detection_variables()
    steering_data = 0
    cam = cv2.VideoCapture(0)
    stm.send_command(aks.Register.MOTOR_POWER,1)

    while not rospy.is_shutdown():
        callback()
        rospy.sleep(0.001)