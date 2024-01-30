#kütüphane tanımlanması
import torch
import time
import cv2 
import pyzed.sl as sl
import sys

#Zed kamera baslatılması
def zedtanimlama():
    zed = sl.Camera()



    # Set configuration parameters
    input_type = sl.InputType()
    if len(sys.argv) >= 2 :
        input_type.set_from_svo_file(sys.argv[1])

    init = sl.InitParameters(input_t=input_type)
    init.camera_resolution = sl.RESOLUTION.HD1080
    #init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    #init.coordinate_units = sl.UNIT.METER



    # Open the camera
    err = zed.open(init)

    if err != sl.ERROR_CODE.SUCCESS :
        print(repr(err))
        print("Kamera baslamiyor")
        return zedtanimlama()
    else:
        return zed,init

zed,init=zedtanimlama()

from threading import Thread, Lock
from keras.models import load_model
from rplidar import RPLidar
from goruntuisleme import goruntuisleme
from serittakibi import serittakibi
from enkoder.ardunio import read
from yenilidarho import teknikKontrol


#GORUNTU ISLEME ICIN YOLOV5 MODELININ YUKLENMESI
custommodel=torch.hub.load("C:\\Users\\evaot\\Desktop\\yolov5-master\\",'custom',"best2.pt",force_reload=False,source="local")
customclasses=custommodel.names

#SERIT TAKIBINI MODELININ TANIMLANMASI
model_serittakibi = load_model(
    "C:\\Users\\evaot\\Desktop\\egitimyarisveriler\\tensorflow-unet-labelme-master_yaris_normalveri\\logs\\the-last-model.h5"
)


#webcam'in tanımlanması
#KAMERAYI KONTROL ETTTTTTTTTTTTT--------------------TTTTTTTTTTTTT-------------
cam = cv2.VideoCapture(2, cv2.CAP_DSHOW)

"""
while True:
    ret, frame = cam.read()
    cv2.imshow("a",frame)
    cv2.waitKey(1)
"""




#LIDAR'in TANIMLANMASI---------PORT KONTROLU
def lidartanimla():
    try:

        lidar = RPLidar('COM5', baudrate=115200)
        time.sleep(2)
        info = lidar.get_info()
        health = lidar.get_health()
        print("info : {}   health : {}      Lidar başlatılıyor...".format(info, health))
        return lidar

    except:
        print("Lidar icin except vakti")
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        return lidartanimla()

lidar=lidartanimla()
print("Lidar tanımlandı")





#Kontrol edilecek parametrelerin tanımlanması


#Enkoder parametreleri
veriyisifirla = [0]
hesapla = [0]
enkoderList = [0]
enkoder_veriler=[veriyisifirla,hesapla,enkoderList]

#LİDAR PARAMETRELERİ
lidaretkin=[0]



#SERIT TAKIBI PARAMETRELERI
ensol=[False]
sol=[False]
sag=[False]
ensag=[False]




#GORUNTU ISLEME PARAMETRELERI


labellar = {'20': 99999, '30': 99999, 'dur':99999,'durak':99999,'girisyok':99999, 'ilerisag':99999, 'ilerisol':99999, 'kirmizi':99999, 'park':99999, 'parkyasak':99999, 'sag':99999, 'sagadonulmez':99999, 'sari':99999, 'sol':99999, 'soladonulmez':99999, 'yesil':99999, 'engellipark':99999, 'tasitrafiginekapali':99999,'yayagecidi':99999}

states={'aracdurdu':False,'aracharekette':True}

goruntuislemeetkin=[0]

#Threadlerin Başlatılması



#Goruntu Isleme
goruntuisleme_thread= Thread(target = goruntuisleme, args = (sl,zed,custommodel,customclasses,labellar,states,enkoder_veriler,goruntuislemeetkin,lidaretkin,ensol,ensag,init))
goruntuisleme_thread.start()


#Lidar
thread_lidar=Thread(target =teknikKontrol , args = (lidar,lidaretkin,enkoder_veriler,goruntuislemeetkin,ensol,ensag))
thread_lidar.start()


#Serittakibi
thread_serittakibi=Thread(target = serittakibi, args = (cam,model_serittakibi,ensol,sol,sag,ensag,lidaretkin,goruntuislemeetkin))
thread_serittakibi.start()

#enkoder
thread_enkoder = Thread(target = read, args = (enkoderList, veriyisifirla, hesapla,))
thread_enkoder.start()   



