
from ultralytics import YOLO
from objetespiti import goruntuisleme
from karar_ver import karar
import cv2 as cv
import pyzed.sl as sl
import sys
from threading import Thread, Lock
import math
import AKS_Communication as aks

stm = aks.STM_Communication("/dev/ttyUSB0")

#Eğitilen YOLOv8 modelinin yüklenmesi
model = YOLO('/home/otonom/Desktop/gitotonom/EVA-Autonomous-Vehicle/levha-tespiti/29.01best.pt')
#Etiketlerin ve onlara karşılık gelen bilginin tutulacağı sözlük yapısı 
custom_classes = model.names
class_names = {'20': 99999, '30': 99999, 'dur':99999,'durak':99999,'girisyok':99999, 'ilerisag':99999, 'ilerisol':99999, 'kirmizi':99999, 'park':99999, 'parkyasak':99999, 'sag':99999, 'sagadonulmez':99999, 'sari':99999, 'sol':99999, 'soladonulmez':99999, 'yesil':99999, 'engellipark':99999, 'tasitrafiginekapali':99999,'yayagecidi':99999, 'kavsak':99999, 'ikiliyon':99999, 'tersengellipark':99999, 'parkYapilmaz':99999}

states={'aracdurdu':False} 
#karar algoritmasında kulanıyoruz bu dictionary yapısını

#baslangıc kilit degişkeninin tanımlanması, kilit değişkeni kamera çalışmaya başladığında 0 olur ve kameradan görüntüyü ekranda da görebilmek adına bu değişkeni kullanacağız
kilid = 1

#resim üreten thread fonksiyonunun tanımı
def kamera(lock):
    global kilid,img_sol,img_lane,img_sag
    
    #Zed kameranın komutları, bu kodlar zed sayfasından alınmıştır.
    
    # ZED kameranın bir nesnesi oluşturuluyor. Bu nesne, ZED kamerayla iletişimi sağlamak için kullanılır.
    zed = sl.Camera()

    # Set configuration parameters
    input_type = sl.InputType()
    if len(sys.argv) >= 2 :
        input_type.set_from_svo_file(sys.argv[1])

    init = sl.InitParameters(input_t=input_type)
    init.camera_resolution = sl.RESOLUTION.HD1080
    init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init.coordinate_units = sl.UNIT.METER

    # Open the camera
    err = zed.open(init)
    if err != sl.ERROR_CODE.SUCCESS :
        print(repr(err))
        print("ZED baslamiyor")

    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.enable_fill_mode = True
    runtime_parameters.confidence_threshold = 100
    runtime_parameters.texture_confidence_threshold = 100

    while True:
        image = sl.Mat()
        depth = sl.Mat()
        point_cloud = sl.Mat()
        imagesag = sl.Mat()
        mirror_ref = sl.Transform()
        mirror_ref.set_translation(sl.Translation(2.75,4.0,0))
        tr_np = mirror_ref.m

        err = zed.grab(runtime_parameters)

        # Sol kameradan gelen görüntüyü almak için kullanılır
        zed.retrieve_image(image, sl.VIEW.LEFT)
        img_sol = image.get_data()

        zed.retrieve_image(imagesag, sl.VIEW.RIGHT)
        img_sag=imagesag.get_data()

        # Retrieve colored point cloud. Point cloud is aligned on the left image.
        zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
        kilid=0
            
        while kilid==0:
        #burada kameradan alınan görüntüyü ekrana yansıtmaya çalışıyoruz
            with lock:
                cv.imshow("Obje Tespiti sol",img_sol)               
            
            if kilid==1:
                with lock:
                    cv.imshow("Obje Tespiti sol",img_sol)
                    cv.waitKey(1)

        if kilid==1:
            with lock:
                cv.imshow("Obje Tespiti sol",img_sol)
                cv.waitKey(1)

lock_cam = Lock()

thread_cam = Thread(target=kamera, args=(lock_cam,))
thread_cam.start()

lock_main = Lock()

while True:

    if kilid==0:
        sagresim=img_sag.copy()
        solresim = img_sol.copy()

        img_pred=cv.cvtColor(solresim,cv.COLOR_BGR2RGB)
        k=0
        results = model(img_pred, stream=True)
        print("obje tespiti yapıldı")
        for r in results:
            boxes = r.boxes
            for box in boxes:
                model_output_class = custom_classes [int(box.cls[0])] #yalnız bir levhayı algılar
                model_output_boundingbox = box.xyxy[0]
                model_output_confidence = math.ceil((box.conf[0]*100))/100
                k = k + 1
        if k>0:
            goruntuisleme(model_output_class, model_output_boundingbox, model_output_confidence, custom_classes, model, k, sagresim, solresim, class_names)
            karar(class_names, states) #karar_algoritması dosyası içerisinde yazdığımız karar fonksiyonunu çağırıyoruz

        with lock_main:
            img_sol=solresim.copy()
            kilid=1