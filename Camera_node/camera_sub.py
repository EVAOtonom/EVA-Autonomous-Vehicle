#!/usr/bin/env python3.9

import rospy
from sensor_msgs.msg import Image as sensor_img
import cv2
from cv_bridge import CvBridge
from keras.models import load_model
import math
import os
import numpy as np
from PIL import Image
import copy
import matplotlib.pyplot as plt
import time
from threading import Thread, Lock
from STM_Communication import send_to_STM
import minimalmodbus

#konumlar her bilgisayar için düzeltilmeli satır 21,260,297

model=load_model("/home/otonom/otonom_ws/src/camera/src/the-last-model.h5")


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
Fonksiyon, verilen görüntüyü 127.5'e böler ve ardından 1 çıkararak görüntüyü -1 ile 1 arasında bir aralığa getirir. (BU ARALIKTA OLDUĞUNDAN NASIL EMİN OLACAĞIZ?)
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
    #nw ve nh, ölçeklendirilmiş genişlik ve yükseklik olarak hesaplanır. ( nw= new weight nh = new height )

    image = image.resize((nw, nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (128, 128, 128))   # gri renk (128,128,128)
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



def detect_image(image_path, yakinmi, model, INPUT_SHAPE , colors):  
    #şerit için görüntü işleme fonksiyonu   # detect_image fonksiyonu, bir görüntü dosyası yolu (image_path) ve bir yakınlık değeri (yakinmi) alır.
    label_names = ['backround', 'ensol', 'sol', 'sag', 'ensag'] #label_names listesi, sınıf etiketlerini içerir.
    threshold = 100
    #threshold değeri, "sol" ve "sag" şeritlerin arasındaki mesafeyi belirleyen bir eşik değeridir. (standart bi değer mi bu değer?)
    image = Image.open(image_path)
    image = cvtColor(image)
    # Görüntü dosyası Image.open yöntemi ile açılır ve daha sonra cvtColor fonksiyonu ile işlenir.
    old_img = copy.deepcopy(image) 
    ori_h = np.array(image).shape[0]
    ori_w = np.array(image).shape[1]
    #copy.deepcopy fonksiyonu kullanılarak bir kopya alınır ve orijinal boyutlar ori_h ve ori_w değişkenlerine atanır.
    image_data, nw, nh = resize_image(image, (INPUT_SHAPE[1], INPUT_SHAPE[0]))
    #resize_image fonksiyonu ile görüntü boyutu belirli bir giriş şekline (INPUT_SHAPE) yeniden boyutlandırılır.
    image_data = normalize(np.array(image_data, np.float32))
    #normalize fonksiyonu, görüntü verilerini belirli bir aralığa ölçeklendirir.
    image_data = np.expand_dims(image_data, 0)
    #np.expand_dims fonksiyonu ile boyut artırma yapılır.
    pr = model.predict(image_data)[0]
    #Model tahmini model.predict ile gerçekleştirilir ve sonuçlar pr değişkenine atanır.
    pr = pr[int((INPUT_SHAPE[0] - nh) // 2):int((INPUT_SHAPE[0] - nh) // 2 +
                                                nh),
            int((INPUT_SHAPE[1] - nw) // 2):int((INPUT_SHAPE[1] - nw) // 2 +
                                                nw)]
    #Gerekli boyutlarda kırpma işlemi yapılır.
    pr = cv2.resize(pr, (ori_w, ori_h), interpolation=cv2.INTER_LINEAR)
    #cv2.resize fonksiyonu ile boyutlar orijinal boyutlara döndürülür.
    pr = pr.argmax(axis=-1)
    #argmax fonksiyonu kullanılarak en yüksek değere sahip sınıf indeksi belirlenir.
    seg_img = np.reshape(
        np.array(colors, np.uint8)[np.reshape(pr, [-1])], [ori_h, ori_w, -1])

    image = Image.fromarray(seg_img)
    #Sonuç görüntü Image.fromarray yöntemi kullanılarak yeniden oluşturulur.

    image = Image.blend(old_img, image, 0.7)
    #Orijinal görüntü ile sonuç görüntü Image.blend yöntemi ile karıştırılır.
    
    #buradan itibaren kodumuzda bize özel kısım başlıyor
    midpoints = {}
    midpoints['backround'] = (0, 0)
    midpoints['ensol'] = (0, 0)
    midpoints['sol'] = (0, 0)
    midpoints['sag'] = (0, 0)
    midpoints['ensag'] = (0, 0)
# Bu bölümde, midpoints adında bir boş sözlük oluşturuluyor. Daha sonra bu sözlüğe bazı anahtar-değer çiftleri ekleniyor.
# Her bir anahtar, arka plan veya farklı etiketlerin temsil ettiği nesneleri belirtir. Örneğin, 
# 'ensol' sol şeridin orta noktasını temsil eder. Koordinatlar (0, 0) olarak başlatılır, çünkü henüz bu bilgilere erişilememiş olabilir.
    areas = {}
    areas['ensol'] = 0
    areas['sol'] = 0
    areas['sag'] = 0
    areas['ensag'] = 0
 #Benzer şekilde, areas adında başka bir boş sözlük oluşturulur ve burada da belirli nesnelerin alanları depolanır. 
 # Her bir anahtar, 'ensol', 'sol', 'sag' ve 'ensag' gibi nesnelerin alanını temsil eder.
 #  Başlangıçta tüm alanlar sıfır olarak ayarlanmıştır, çünkü henüz bu alanlara dair veri elde edilmemiş olabilir.
    """midpoints ve areas adında iki sözlük oluşturuluyor. Bu sözlükler, nesnelerin merkez noktalarını ve alanlarını depolamak için kullanılır."""
    endpoints = {}
    endpoints['ensol'] = ((0, 0), (0, 0))
    endpoints['sol'] = ((0, 0), (0, 0))
    endpoints['sag'] = ((0, 0), (0, 0))
    endpoints['ensag'] = ((0, 0), (0, 0))
# endpoints sözlüğü, 'ensol', 'sol', 'sag' ve 'ensag' gibi nesnelerin uç noktalarının koordinatlarını depolar. 
# Her bir anahtarın değeri, başlangıçta ((0, 0), (0, 0)) olarak belirlenir, çünkü bu koordinatlar henüz elde edilmemiş olabilir.
    # nesnenin ("ensol", "sol", "sag" ...) uç noktalarının koordinatları depolanır. 

#Bu kod parçaları, ilgili verilerin depolanması için kullanılan sözlüklerin oluşturulmasını ve başlangıç değerlerinin atanmasını gösterir.
#  Bu veriler, sonraki işlemlerde kullanılmak üzere saklanır ve güncellenir.
    img = np.array(image)
#Bu satır, 'image' adlı görüntüyü NumPy dizisine dönüştürür ve 'img' adında bir değişkene atar. 
# Bu dönüşüm, daha sonra kullanılmak üzere görüntü verilerinin bir NumPy dizisinde depolanmasını sağlar.
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
# """ 
# Bu döngü, etiketlerin sınıflarına göre işlem yapar. pr dizisindeki her bir elemanın sınıfı kontrol edilir.
#  Sınıf etiketinin indeksi c olarak atanır ve bu sınıfın görüntüdeki koordinatları bulunur.
# Bu koordinatlar, np.where fonksiyonu kullanılarak alınır. Ardından, bu sınıfın alanı hesaplanır ve bir değişkene atılır.

# Eğer bu alan belirli bir eşik değerinden küçükse (area<150 gibi), işleme devam edilmez. 
# Bu satır şu anlık yorum içerisindedir, yani bu kısımdaki kod çalıştırılmaz.

# Daha sonra, eğer 'y' ve 'x' dizilerinin uzunlukları 0 ise veya sıfıra eşitse, işlem devam ettirilmez.
# Yani, eğer bu sınıfın pikselleri bulunamazsa veya koordinatları 0 ise, işlem atlanır.

# Eğer yukarıdaki koşullar sağlanmazsa, bu sınıfın alanı ve merkez noktası ilgili sözlüklerdeki değerler güncellenir.

# """ 


        # Find the points with the maximum and minimum y values
        max_y_idx = np.argmax(y)
        min_y_idx = np.argmin(y)
        max_y_point = (x[max_y_idx], y[max_y_idx])
        min_y_point = (x[min_y_idx], y[min_y_idx])
        #En yüksek ve en düşük y değerine sahip noktaları bulur. Bu, nesnelerin üst ve alt sınırlarını belirlemeye yardımcı olur.

        endpoints[label_names[c]] = {'max_y': max_y_point, 'min_y': min_y_point}
        #Her nesne için endpoints adlı bir sözlüğe maksimum ve minimum y noktalarını kaydeder.
        
        if label_names[c]=='sol' or label_names[c]=='sag':
# eğer sınıf etiketi 'sol' veya 'sag' ise, içerideki bloğun çalıştırılacağını belirtir.
            if label_names[c]=='sag':
#eğer sınıf etiketi 'sag' ise, içerideki bloğun çalıştırılacağını belirtir.
                cv2.circle(img, (endpoints[label_names[c]]['max_y'][0], endpoints[label_names[c]]['max_y'][1]), 10, (0, 255, 0), -1)
#Bu satır, 'cv2.circle' fonksiyonunu kullanarak 'img' üzerinde bir daire çizer. Bu daire, 'sag' sınıfının en yüksek 'y' noktasına, 
# yeşil renk ile ve yarıçapı 10 olan bir daire olarak çizilir.
                cv2.putText(img, 'sag',(endpoints[label_names[c]]['max_y'][0], endpoints[label_names[c]]['max_y'][1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#Bu satır, 'cv2.putText' fonksiyonunu kullanarak 'img' üzerine bir metin ekler.
# Bu metin, 'sag' olarak belirlenmiş ve 'sag' sınıfının en yüksek 'y' noktasının hemen altında görüntülenir.

                #Belirli etiketler ('sol' veya 'sag' gibi) için özel durumlar oluşturur. Eğer etiket 'sag' ise, ilgili nesnenin üst noktasını yeşil bir daire ile işaretler ve üzerine 'sag' yazısı ekler. 
                #Eğer etiket 'sol' ise, ilgili nesnenin üst noktasını yeşil bir daire ile işaretler ve üzerine 'sol' yazısı ekler. Her iki durumda da, nesnenin alt noktasını yeşil bir daire ile işaretler.
                
                cv2.circle(img, (endpoints[label_names[c]]['min_y'][0], endpoints[label_names[c]]['min_y'][1]), 10, (0, 255, 0), -1)
#cv2.circle fonksiyonu kullanılarak 'img' üzerinde bir daire çizer. 
# Bu daire 'sol' veya 'sag' sınıfının en düşük 'y' noktasına, yeşil renk ile ve yarıçapı 10 olan bir daire olarak çizilir.

            if label_names[c]=='sol':
#eğer sınıf etiketi 'sol' ise, içerideki bloğun çalıştırılacağını belirtir.
                cv2.circle(img, (endpoints[label_names[c]]['max_y'][0], endpoints[label_names[c]]['max_y'][1]), 10, (0, 255, 0), -1)
                cv2.putText(img, 'sol', (endpoints[label_names[c]]['max_y'][0], endpoints[label_names[c]]['max_y'][1]+20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                cv2.circle(img, (endpoints[label_names[c]]['min_y'][0], endpoints[label_names[c]]['min_y'][1]), 10, (0, 255, 0), -1)
#'sol' sınıf etiketi için belirli noktalara daireler çizer ve bu dairelerin üzerine metin ekler. 
#'max_y' ve 'min_y' noktaları üzerine daireler çizilir ve bu noktaların hemen üstünde ve altında 'sol' metni görüntülenir.

    

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
# Bu döngü, 'midpoints' sözlüğündeki her bir öğe için işlem yapar. 'midpoints' sözlüğü, nesnelerin merkez noktalarını içerir.
# 'label' ve 'midpoint' değişkenleri, sırasıyla etiket adını ve merkez noktanın koordinatlarını temsil eder.
# Bu koordinatlara göre, her bir nesnenin merkezine bir daire çizilir ve nesnenin etiketi ile birlikte görüntüye eklenir. 
# Ayrıca, nesnenin alanı da bu işlemde görüntüye eklenir.
    if label_names[2] in midpoints and label_names[3] in midpoints:
        distance = abs(midpoints['sol'][1] - midpoints['sag'][1])
        if distance < threshold:
            yakinmi = 1
            cv2.putText(img, 'label "sag" and "sol" are too close',
                        (x + 15, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)
    return img, midpoints, yakinmi, areas, endpoints


def cam_callback(data):
    #fps = time.time()
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(data)
    cv2.imwrite("/home/otonom/otonom_ws/src/camera/src/frame.jpg",img)
    zaman = time.time()

    colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128),
          (128, 0, 128), (0, 128, 128), (128, 128, 128),
          (64, 0, 0), (192, 0, 0), (64, 128, 0), (192, 128, 0), (64, 0, 128),
          (192, 0, 128), (64, 128, 128), (192, 128, 128), (0, 64, 0),
          (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128),
          (128, 64, 12)]

    INPUT_SHAPE = [480, 640, 3]  # (H, W, C)

    # eğitilmiş modelin yuklenmesi sağlanır.


    #BASLANGIC PARAMETTRELERININ YUKLENMESI
    guvenaraligi = 5
    aracdurdumu=[0]
    eskidonmeacisi = 00

    p = 0
    i = 0
    d = 0
    dt = 0
    kp = 0.5
    kd = 0
    ki = 0
    cagırma = 0

    """
    KalmanFilter adında bir nesne oluşturulduktan sonra, bir döngü başlatır.
    Döngü, 'yakinmi' değişkenine başlangıçta 0 değerini atar. Ardından, kameradan bir kare okur ve bu kare üzerinde işlem yapar. 
    Eğer 'aracdurdumu' listesinin ilk elemanı 1 ise, döngüyü sonlandırır. Ayrıca, 'cagırma' değişkeni 0 ise, döngü devam eder. 
    """
    yakinmi = 0 
    baslangıc_zamani = time.time()
    #/home/sefa/catkin_ws/src/camera/src/frame
    image, midpoints, yakinmi, areas, endpoints = detect_image("/home/otonom/otonom_ws/src/camera/src/frame.jpg", yakinmi, model, INPUT_SHAPE, colors)
    if aracdurdumu[0]==1:
        print("aracdurumu[0] == 1")
        return
    if cagırma == 0:

# Kod, döngü içinde görüntü işleme işlevlerini çağırır ve sonuçları işler. 
# 'aracdurdumu' listesinin durumuna bağlı olarak döngüyü sonlandırır veya devam ettirir. 
# 'cagırma' değişkeninin durumu da döngünün devam etmesi veya sonlanması üzerinde etkili olabilir.

        cagırma = 1
        time.sleep(0.3)
    if areas['sol'] <= 50:
        midpoints['sol'] = (0, 0)

    if areas['sag'] <= 50:
        midpoints['sag'] = (0, 0)

    #print(f"iki serit yakın mı?   {yakinmi}")
    image = np.array(image)
    image = image[:, :, ::-1].copy()
    # print(midpoints['sol'])
    # print(midpoints['sag'])
    # print(midpoints['ensol'])
    # print(midpoints['ensag'])
    # print(f"sol uc noktaları: {endpoints['sol']}")
    # print(f"sag uc noktaları: {endpoints['sag']}")
    orta_y = 0
    orta_x = 0
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

# Bu kod parçacığı, 'midpoints' ve 'yakinmi' değişkenlerinin değerlerine dayalı olarak çeşitli hesaplamalar yapar.
#  İlk olarak, 'sol' ve 'sag' seritlerinin x ve y değerlerinin 0 olmadığı koşulu kontrol eder. 
#  Daha sonra 'yakinmi' değişkeninin 1'e eşit olup olmadığını kontrol eder. 
#  Eğer bu koşullar sağlanırsa, 'orta_serit_x' ve 'orta_y' değerlerini hesaplar.

# Daha sonra, 'endpoints' sözlüğünde belirli değerlere göre koşullar kontrol edilir. 
# 'orta_x' ve 'orta_y' değerleri, 'orta_serit_x' ve 'midpoints' değerlerinin bir fonksiyonu olarak belirlenir. 
# 'endpoints' sözlüğündeki değerlere bağlı olarak, 'orta_x' değeri belirli bir şekilde hesaplanır.

# Kodda orta_x ve orta_y değerleri şeritlerin konumlarına ilişkin hesaplamalarda kullanılır.

# orta_serit_x, 'sol' ve 'sağ' şeritlerinin x koordinatlarının ortalamasıdır. Bu değer, şeritlerin genel konumunu belirlemeye yardımcı olur.
# orta_x, 'orta_serit_x' değerine dayalı olarak belirlenir. 'orta_serit_x' değerine 400 eklenir veya 400 çıkarılır. Bu, şeritlerin merkezine göre bir konum sağlamak için yapılır. Yani eğer 'sag' şeridinin sağ ucu 'sol' şeridinin sol ucundan daha ilerideyse, 'orta_x' değeri 400 eklenir, aksi halde 400 çıkarılır. Bu, aracın yönünü belirlemede kullanılabilir.
# orta_y, 'sol' ve 'sağ' şeritlerinin y koordinatlarının ortalamasıdır. Bu, şeritlerin yüksekliği veya y eksenindeki konumları hakkında bilgi verir.

# Bu hesaplamalar, aracın şeritler arasında konumunu belirlemesine yardımcı olur ve bu bilgiler daha sonra aracın hareketini düzenlemek için PID kontrolü gibi diğer hesaplamalarda kullanılabilir.

            
            if orta_serit_x > image.shape[1] / 2:
                orta_x = -400 + orta_serit_x
                orta_y = (midpoints['sol'][0] + midpoints['sag'][0]) / 2
            if orta_serit_x < image.shape[1] / 2:
                orta_x = -400 + orta_serit_x
                orta_y = (midpoints['sol'][0] + midpoints['sag'][0]) / 2
            
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
#  """ 
#  if orta_serit_x > image.shape[1] / 2: ve if orta_serit_x < image.shape[1] / 2:: Bu if-else bloğu, orta seridin görüntünün 
#  yarısından büyük veya küçük olmasını kontrol eder. Eğer orta serit, görüntünün sol yarısında ise, orta_x değeri -400 eklenerek belirlenir. 
#  Eğer orta serit, görüntünün sağ yarısında ise, orta_x değeri 400 çıkarılarak belirlenir.
#    orta_y değeri ise 'sol' ve 'sağ' şeritlerinin y koordinatlarının ortalamasını alır.
# else:: Eğer orta serit, görüntünün yarısına eşitse, orta_y ve orta_x değerleri, 'sol' ve 'sağ' şeritlerinin ortalamasını alır.
# Her durumda, çizgilerin çizilmesi işlemi gerçekleşir. İlk cv2.line() fonksiyonu, görüntünün ortasından başlayarak orta_y'ye bir çizgi çizer. 
# İkinci ve üçüncü cv2.line() fonksiyonları ise orta_x ve orta_y noktaları arasında bir çizgi çizer.
# elif midpoints['sag'] == (0, 0) and midpoints['sol'] != (0, 0): ve elif midpoints['sol'] == (0, 0) and midpoints['sag'] != (0, 0): blokları, 
# sırasıyla 'sağ' ve 'sol' şeritlerin birinin görüntüde olmadığı durumları kontrol eder. Bu durumlarda, çizgilerin çizilmesi işlemi gerçekleşir.
# else:: Eğer hiçbir şerit yoksa, "ucgen cizilemedi" yazdırılır
#  """ 
    uzaklik_y = (image.shape[0] - orta_y)  #kameranın orta noktasından şerit orta noktası çıkarma
    uzaklik_x = (
        ((image.shape[1] / 2)+30) - orta_x
    )  #kameradan gelen görüntünün widthini 2 ye böl orta noktasını bul şeridin orta noktasından çıkar.
    donme_acisi = (180 * math.atan(abs(uzaklik_x / uzaklik_y))) / (3.14)

    donme_acisi = int(donme_acisi * 53 / 10)
#  """"""
#  uzaklik_y" değişkeni, kameranın orta noktasından şerit orta noktasının çıkarılmasıyla hesaplanır.
# "uzaklik_x" değişkeni, kameradan gelen görüntünün genişliğini 2'ye böler, ardından orta noktayı bulur ve şeridin orta noktasından çıkarır.
# "donme_acisi" değişkeni, bu iki uzaklık değeri kullanılarak hesaplanır. İlk olarak, bu iki uzaklık değeri arasındaki arctan işlemi kullanılarak bir açı hesaplanır.
#  Bu açı, daha sonra 180'e bölünür ve 3.14'e bölünerek radyan cinsinden ifade edilir.
# Son olarak, "donme_acisi" değeri belirli bir formül kullanılarak tekrar hesaplanır ve tam sayıya dönüştürülür.
#  """"""
    if True :
        try:
            send_to_STM(2,1, instrument)
            zaman = time.time()
            dt = time.time() - zaman
            if dt == 0:
                    dt = 60.0 
            
            p = kp * donme_acisi
            i = i + ki * donme_acisi * dt
            d = kd * (donme_acisi - eskidonmeacisi) / dt #368.satırda ve 370'te donme_acisinin hesaplanisi var
            eskidonmeacisi = donme_acisi
            pid = int(p + i + d)

            if uzaklik_x < 0:
                if  pid >= 100:
                    pid = 100
                print(pid)                                
                pid = (pid / 3) # sağa döner
                #csv_yaz(pid)#csv dosyasina, gönderilen tekerlek açısını, gönderildiği dakika ve saniyeyi yazacak fonksiyonu buraya yazınız. 
                send_to_STM(0,pid, instrument)
               

            if uzaklik_x > 0:

             # Araç sağda, sola dön
                if pid >= 100:
                    pid = 100
                print(-pid)
                pid = -(pid / 3)  #sola döner
                #csv_yaz(pid)#csv dosyasina, gönderilen tekerlek açısını, gönderildiği dakika ve saniyeyi yazacak fonksiyonu buraya yazınız. 
                send_to_STM(0,pid, instrument)

        except ZeroDivisionError:
            dt = 1.0
            zaman = time.time()
            p = kp * donme_acisi
            pid = int(p)
            
            if uzaklik_x < 0:           

                if  pid >= 100:
                    pid = 100
                print(pid)                    
                pid = pid /3      #sağa döner 
                #csv_yaz(pid)#csv dosyasina, gönderilen tekerlek açısını, gönderildiği dakika ve saniyeyi yazacak fonksiyonu buraya yazınız. 
                send_to_STM(0,pid, instrument)

                 

            if uzaklik_x > 0:

                if pid >= 100:
                    pid = 100
                print(-pid)    
                pid = pid /3    #sola döner.
                #csv_yaz(pid)#csv dosyasina, gönderilen tekerlek açısını, gönderildiği dakika ve saniyeyi yazacak fonksiyonu buraya yazınız. 
                send_to_STM(0,pid, instrument)
    else:
        p = 0
        i = 0
        d = 0
        dt = 0
    cv2.imshow("otonom",image)
    #print(time.time()-fps)
    cv2.waitKey(1)

def camera_subscriber():
    rospy.init_node("camera_subscriber", anonymous=True)
    rospy.Subscriber("camera_scan", sensor_img, cam_callback)
    rospy.spin()

if __name__ == "__main__":
    try:
        instrument = minimalmodbus.Instrument('/dev/ttyUSB0', slaveaddress=1)
        instrument.serial.baudrate = 38400
        send_to_STM(2, 2, instrument)
        camera_subscriber()
    except rospy.ROSInterruptException:
        pass
