from keras.models import load_model
import math
import os
import numpy as np
from PIL import Image
import cv2
import copy
import matplotlib.pyplot as plt
import time
from aks_communication import sendToArduino
from threading import Thread, Lock

colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128),
          (128, 0, 128), (0, 128, 128), (128, 128, 128),
          (64, 0, 0), (192, 0, 0), (64, 128, 0), (192, 128, 0), (64, 0, 128),
          (192, 0, 128), (64, 128, 128), (192, 128, 128), (0, 64, 0),
          (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128),
          (128, 64, 12)]

INPUT_SHAPE = [480, 640, 3]  # (H, W, C)

"""INPUT_SHAPE değişkeni, modelin beklediği giriş görüntüsünün boyutunu temsil eder. Bu boyut üç bileşen içerir:

H: Görüntünün yüksekliği (height)
W: Görüntünün genişliği (width)
C: Görüntünün kanal sayısı (channels). Bu genellikle renk kanalları için 3 (RGB) veya siyah-beyaz görüntülerde 1 (grayscale) olarak ayarlanır.
"""

def cvtColor(image):
    if len(np.shape(image)) == 3 and np.shape(image)[-2] == 3:
        return image
    else:
        image = image.convert('RGB')
        return image

"""
Eğer görüntü 3 boyutlu ve ikinci boyutun uzunluğu 3 ise (yani renk kanalları RGB ise), görüntü zaten doğru renk formatındadır. 
Bu durumda görüntü doğrudan döndürülür (return image).

Eğer yukarıdaki koşul sağlanmazsa, yani görüntü farklı bir renk formatına sahipse, image.convert('RGB') ifadesi görüntüyü 
RGB renk formatına dönüştürür ve dönüştürülmüş görüntü döndürülür.

Bu kod parçası, görüntüyü işleme işlemine geçmeden önce görüntünün doğru renk formatına sahip olmasını sağlamak için kullanılır.

Görüntü işleme algoritmaları ve modelleri genellikle belirli bir renk formatını beklerler ve bu formatın dışındaki görüntülerle doğru sonuçlar üretemezler. 
Bu nedenle, işleme öncesinde görüntünün doğru renk formatına sahip olduğundan emin olmak önemlidir.
"""

def normalize(image):
    image = image / 127.5 - 1
    return image

""" 
Fonksiyon, verilen görüntüyü 127.5'e böler ve ardından 1 çıkararak görüntüyü -1 ile 1 arasında bir aralığa getirir. 
Bu genellikle Convolutional Neural Networks (CNN) gibi derin öğrenme modellerinin daha iyi performans göstermesine yardımcı olabilir.
"""

def resize_image(image, size):
    iw, ih = image.size
    w, h = size

    scale = min(w / iw, h / ih)
    #scale, orijinal boyut ile hedef boyut arasında minimum ölçekteki oranı belirler. 
    #Bu oran, etiket görüntüsünün hem yatayda hem de dikeyde ne kadar ölçeklendirilmesi gerektiğini belirler.
    nw = int(iw * scale)
    nh = int(ih * scale)
    #nw ve nh, ölçeklendirilmiş genişlik ve yükseklik olarak hesaplanır.

    image = image.resize((nw, nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (128, 128, 128))
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))

    return new_image, nw, nh
"""Bu fonksiyon, verilen görüntüyü istenen şekilde yeniden boyutlandırmak için kullanılır."""


def resize_label(image, size):
#Bu fonksiyon, etiket görüntülerini belirli bir boyuta yeniden boyutlandırmak ve işlemek için kullanılır. Genellikle model eğitimi sırasında girdi görüntülerinin boyutlarını değiştirirken, etiket görüntülerinin de aynı oranda yeniden boyutlandırılması gerekmektedir. 
#Bu fonksiyon, bu yeniden boyutlandırma işlemini gerçekleştirirken uygun etiketlerin korunmasını sağlamak için kullanılır.
    iw, ih = image.size
    w, h = size
    #iw ve ih, orijinal etiket görüntüsünün genişliği ve yüksekliği olarak alınır.
    #w ve h, hedef boyutun genişliği ve yüksekliği olarak alınır.
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)

    image = image.resize((nw, nh), Image.NEAREST)
    #Orijinal etiket görüntüsü, belirtilen ölçekte yeniden boyutlandırılır.
    new_image = Image.new('L', size, (0))
    #new_image, hedef boyut ve siyah (0 değerine sahip) piksellerden oluşan bir görüntü oluşturur.
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
    #Ölçeklendirilmiş etiket görüntüsü, bu yeni görüntüye, orijinal etiket görüntüsünün merkezine yerleştirilir.

    return new_image, nw, nh


def detect_image(image_path, yakinmi):
    #şerit için görüntü işleme fonksiyonu
    label_names = ['backround', 'ensol', 'sol', 'sag', 'ensag']
    threshold = 100
    #threshold değeri, "sol" ve "sag" şeritlerin arasındaki mesafeyi belirleyen bir eşik değeridir.
    image = Image.open(image_path)
    image = cvtColor(image)

    old_img = copy.deepcopy(image)
    ori_h = np.array(image).shape[0]
    ori_w = np.array(image).shape[1]

    image_data, nw, nh = resize_image(image, (INPUT_SHAPE[1], INPUT_SHAPE[0]))

    image_data = normalize(np.array(image_data, np.float32))

    image_data = np.expand_dims(image_data, 0)

    pr = model.predict(image_data)[0]

    pr = pr[int((INPUT_SHAPE[0] - nh) // 2):int((INPUT_SHAPE[0] - nh) // 2 +
                                                nh),
            int((INPUT_SHAPE[1] - nw) // 2):int((INPUT_SHAPE[1] - nw) // 2 +
                                                nw)]

    pr = cv2.resize(pr, (ori_w, ori_h), interpolation=cv2.INTER_LINEAR)

    pr = pr.argmax(axis=-1)

    seg_img = np.reshape(
        np.array(colors, np.uint8)[np.reshape(pr, [-1])], [ori_h, ori_w, -1])

    image = Image.fromarray(seg_img)

    image = Image.blend(old_img, image, 0.7)
    
    #buradan itibaren kodumuzda bize özel kısım başlıyor
    midpoints = {}
    midpoints['backround'] = (0, 0)
    midpoints['ensol'] = (0, 0)
    midpoints['sol'] = (0, 0)
    midpoints['sag'] = (0, 0)
    midpoints['ensag'] = (0, 0)
    areas = {}
    areas['ensol'] = 0
    areas['sol'] = 0
    areas['sag'] = 0
    areas['ensag'] = 0
    """midpoints ve areas adında iki sözlük oluşturuluyor. Bu sözlükler, nesnelerin merkez noktalarını ve alanlarını depolamak için kullanılır."""
    endpoints = {}
    endpoints['ensol'] = ((0, 0), (0, 0))
    endpoints['sol'] = ((0, 0), (0, 0))
    endpoints['sag'] = ((0, 0), (0, 0))
    endpoints['ensag'] = ((0, 0), (0, 0))
    # nesnenin ("ensol", "sol", "sag" ...) uç noktalarının koordinatları depolanır. 

    img = np.array(image)
    for c in range(5):
        y, x = np.where(pr == c)
        area = len(y)
        """
        if area<150:
            continue
        """
        if len(y) == 0 or len(x) == 0:
            continue

        areas[label_names[c]] = len(y)
        midpoints[label_names[c]] = (int(np.mean(y)), int(np.mean(x)))



        # Find the points with the maximum and minimum y values
        max_y_idx = np.argmax(y)
        min_y_idx = np.argmin(y)
        max_y_point = (x[max_y_idx], y[max_y_idx])
        min_y_point = (x[min_y_idx], y[min_y_idx])
        #En yüksek ve en düşük y değerine sahip noktaları bulur. Bu, nesnelerin üst ve alt sınırlarını belirlemeye yardımcı olur.

        endpoints[label_names[c]] = {'max_y': max_y_point, 'min_y': min_y_point}
        #Her nesne için endpoints adlı bir sözlüğe maksimum ve minimum y noktalarını kaydeder.
        
        if label_names[c]=='sol' or label_names[c]=='sag':

            if label_names[c]=='sag':

                cv2.circle(img, (endpoints[label_names[c]]['max_y'][0], endpoints[label_names[c]]['max_y'][1]), 10, (0, 255, 0), -1)
                cv2.putText(img, 'sag',(endpoints[label_names[c]]['max_y'][0], endpoints[label_names[c]]['max_y'][1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                #Belirli etiketler ('sol' veya 'sag' gibi) için özel durumlar oluşturur. Eğer etiket 'sag' ise, ilgili nesnenin üst noktasını yeşil bir daire ile işaretler ve üzerine 'sag' yazısı ekler. 
                #Eğer etiket 'sol' ise, ilgili nesnenin üst noktasını yeşil bir daire ile işaretler ve üzerine 'sol' yazısı ekler. Her iki durumda da, nesnenin alt noktasını yeşil bir daire ile işaretler.
                
                cv2.circle(img, (endpoints[label_names[c]]['min_y'][0], endpoints[label_names[c]]['min_y'][1]), 10, (0, 255, 0), -1)


            if label_names[c]=='sol':

                cv2.circle(img, (endpoints[label_names[c]]['max_y'][0], endpoints[label_names[c]]['max_y'][1]), 10, (0, 255, 0), -1)
                cv2.putText(img, 'sol', (endpoints[label_names[c]]['max_y'][0], endpoints[label_names[c]]['max_y'][1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                cv2.circle(img, (endpoints[label_names[c]]['min_y'][0], endpoints[label_names[c]]['min_y'][1]), 10, (0, 255, 0), -1)


    

    for label, midpoint in midpoints.items():
        #print(label)
        #print(areas[label])
        y, x = midpoint
        if label == 'backround':
            continue
        cv2.circle(img, (x, y), 10, (0, 255, 0), -1)
        cv2.putText(img, label, (x + 15, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.putText(img, 'area: ' + str(areas[label]), (x, y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    if label_names[2] in midpoints and label_names[3] in midpoints:
        distance = abs(midpoints['sol'][1] - midpoints['sag'][1])
        if distance < threshold:
            yakinmi = 1
            cv2.putText(img, 'label "sag" and "sol" are too close',
                        (x + 15, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)
    return img, midpoints, yakinmi, areas, endpoints


cam = cv2.VideoCapture(3, cv2.CAP_DSHOW)
#cam = cv2.VideoCapture("C:\\Users\\Lenovo\\Desktop\\f.mp4")

"""# Kameraya erişim sağla
cam = cv2.VideoCapture(0)

# Sonsuz bir döngüde kameradan görüntü al
while True:
    ret, frame = cam.read()  # Görüntüyü yakala
    cv2.imshow('Kamera Görüntüsü', frame)  # Görüntüyü göster
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' tuşuna basıldığında döngüyü kır
        break"""

#model = load_model("C:\\Users\\Lenovo\\Desktop\\logs\\the-last-model.h5")
model=load_model("C:\\Users\\evaot\\Desktop\\tf-unet-labelme-lane detection\\logs\\the-last-model.h5")

#BASLANGIC PARAMETTRELERININ YUKLENMESI
guvenaraligi = 5
"""
ki=0.005#belirlenecek test sonucuna göre
kd=0.1#belirlenecek test sonucuna göre
kp=0.5#belirlenecek test sonucuna göre
"""
aracdurdumu=[0]
eskidonmeacisi = 00
p = 0
i = 0
d = 0
dt = 0
kp = 1 / 2
kd = 0
ki = 0
cagırma = 0
olcum = KalmanFilter(55, 62, 0.1)
while True:
    yakinmi = 0
    baslangıc_zamani = time.time()
    ret, frame = cam.read()
    #frame=cv2.imread("41.jpg")
    cv2.imwrite("frame.jpg", frame)
    image, midpoints, yakinmi, areas, endpoints = detect_image("frame.jpg", yakinmi)
    if aracdurdumu[0]==1:
        break
    if cagırma == 0:

        #write_read('w70\n')
        cagırma = 1
        time.sleep(0.3)
    if areas['sol'] <= 50:
        midpoints['sol'] = (0, 0)

    if areas['sag'] <= 50:
        midpoints['sag'] = (0, 0)

    print(f"iki serit yakın mı?   {yakinmi}")
    image = np.array(image)
    image = image[:, :, ::-1].copy()
    print(midpoints['sol'])
    print(midpoints['sag'])
    print(midpoints['ensol'])
    print(midpoints['ensag'])
    print(f"sol uc noktaları: {endpoints['sol']}")
    print(f"sag uc noktaları: {endpoints['sag']}")

    if float(
        (midpoints['sol'][1]) != 0 or float(midpoints['sol'][0]) != 0
    ) and (float(midpoints['sag'][1]) != 0 or float(midpoints['sag'][0])) != 0:
        if yakinmi == 1:

            orta_serit_x = (midpoints['sol'][1] + midpoints['sag'][1]) / 2

            if endpoints['sag']['max_y'][0]-endpoints['sag']['min_y'][0]<0:
                orta_x = 400 + orta_serit_x
                orta_y = (midpoints['sol'][0] + midpoints['sag'][0]) / 2

            if endpoints['sag']['max_y'][0]-endpoints['sag']['min_y'][0]>0:
                orta_x = -400 + orta_serit_x
                orta_y = (midpoints['sol'][0] + midpoints['sag'][0]) / 2

            """ 
            if orta_serit_x > image.shape[1] / 2:
                orta_x = -400 + orta_serit_x
                orta_y = (midpoints['sol'][0] + midpoints['sag'][0]) / 2
            if orta_serit_x < image.shape[1] / 2:
                orta_x = -400 + orta_serit_x
                orta_y = (midpoints['sol'][0] + midpoints['sag'][0]) / 2
            """
             
        else:
            #print('Ucgen cizildi')
            orta_y = (midpoints['sol'][0] + midpoints['sag'][0]) / 2
            orta_x = (midpoints['sol'][1] + midpoints['sag'][1]) / 2

        image = cv2.line(image, (int((image.shape[1] / 2))+30, int(image.shape[0])),
                         ((int(image.shape[1] / 2))+30, int(orta_y)), (0, 255, 0),
                         2)
        image = cv2.line(image, ((int(image.shape[1] / 2))+30, int(image.shape[0])),
                         (int(orta_x), int(orta_y)), (0, 255, 0), 2)
        image = cv2.line(image, ((int(image.shape[1] / 2))+30, int(orta_y)),
                         (int(orta_x), int(orta_y)), (0, 255, 0), 2)
    elif midpoints['sag'] == (0, 0) and midpoints['sol'] != (0, 0):
        orta_y = midpoints['sol'][0]
        orta_x = midpoints['sol'][1] + 400
        image = cv2.line(image, ((int(image.shape[1] / 2))+30, int(image.shape[0])),
                         ((int(image.shape[1] / 2))+30, int(orta_y)), (0, 255, 0),
                         2)
        image = cv2.line(image, ((int(image.shape[1] / 2))+30, int(image.shape[0])),
                         (int(orta_x), int(orta_y)), (0, 255, 0), 2)
        image = cv2.line(image, ((int(image.shape[1] / 2))+30, int(orta_y)),
                         (int(orta_x), int(orta_y)), (0, 255, 0), 2)

    elif midpoints['sol'] == (0, 0) and midpoints['sag'] != (0, 0):
        orta_y = midpoints['sag'][0]
        orta_x = midpoints['sag'][1] - 400
        image = cv2.line(image, ((int(image.shape[1] / 2))+30, int(image.shape[0])),
                         ((int(image.shape[1] / 2))+30, int(orta_y)), (0, 255, 0),
                         2)
        image = cv2.line(image, ((int(image.shape[1] / 2))+30, int(image.shape[0])),
                         (int(orta_x), int(orta_y)), (0, 255, 0), 2)
        image = cv2.line(image, ((int(image.shape[1] / 2))+30, int(orta_y)),
                         (int(orta_x), int(orta_y)), (0, 255, 0), 2)

    else:
        print('ucgen cizilemedi')
        continue

    uzaklik_y = (image.shape[0] - orta_y
                 )  #kameranın orta noktasından şerit orta noktası çıkarma
    uzaklik_x = (
        ((image.shape[1] / 2)+30) - orta_x
    )  #kameradan gelen görüntünün widthini 2 ye böl orta noktasını bul şeridin orta noktasından çıkar.
    donme_acisi = (180 * math.atan(abs(uzaklik_x / uzaklik_y))) / (3.14)

    donme_acisi = int(donme_acisi * 53 / 10)
    
    if True :

        try:
            
            """image = cv2.putText(image, 'pid ye girdim', (640, 360), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,
                                cv2.LINE_AA)"""
            dt = time.time() - zaman
            p = kp * donme_acisi
            i = i + ki * donme_acisi * dt
            d = kd * (donme_acisi - eskidonmeacisi) / dt #368.satırda ve 370'te donme_acisinin hesaplanisi var
            eskidonmeacisi = donme_acisi
            pid = int(p + i + d)
            zaman = time.time()

            if uzaklik_x < 0:
                if pid >= 99:
                    pid = 95

                pid = str(pid)
                pid = "t-" + pid + "\n" #açı göndereceğiz pid değerine göre - açı olduğu için araç sağa dönecek
                print(pid)
                write_read(pid)

            if uzaklik_x > 0:
                if pid >= 99:
                    pid = 95

                pid = str(pid)
                pid = "t" + pid + "\n" #açı göndereceğiz pid değerine göre araç sola dönecek
                print(pid)
                write_read(pid)

        except:
            zaman = time.time()
            p = kp * donme_acisi
            pid = int(p)
            if uzaklik_x < 0:

                #arac sola donecek
                print("pid değeri", pid)

                if pid >= 99:
                    pid = 95
                print(pid)

                pid = str(pid)
                pid = "t-" + pid + "\n"
                print(pid)

                write_read(pid)

            if uzaklik_x > 0:
                #arac saga donecek
                print("pid değeri", pid)
                if pid >= 99:
                    pid = 95

                pid = str(pid)
                pid = "t" + pid + "\n"
                print(pid)

                write_read(pid)

    else:
        p = 0
        i = 0
        d = 0
        dt = 0 

    cv2.imshow("image", image)
    cv2.waitKey(1)
    os.remove('frame.jpg')

    #print("FPS:       ",1/(time.time()-baslangıc_zamani))