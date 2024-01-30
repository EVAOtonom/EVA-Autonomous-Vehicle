
from enkoder.ilerleme import predict_ileri
from enkoder.ilerleme import predict_yonlendirme
import serial
import time
from threading import Thread, Lock
import pickle


from enkoder.ardunio import readAciEnkoder

#ardunio = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

#time.sleep(2)



model_ileri_linear = pickle.load(open("ilerlemeLinear4.pickle","rb"))
model_ileri_poly = pickle.load(open("ilerlemePoly4.pickle","rb"))

model_yanal_linear = pickle.load(open("yonlenmeLinear4.pickle","rb"))
model_yanal_poly = pickle.load(open("yonlenmePoly4.pickle","rb"))



def read(ilerlemeList,yonlenmeList,veriyisifirla,hesapla):
    global ardunio
    global model_ileri_linear, model_ileri_poly,model_yanal_linear,model_yanal_poly
    enkoder_son_veri=0
    enkoder_eski_veri=0
    hizlar=[]
    while True:
        try:
            
            aci,enkoder=readAciEnkoder(ardunio)
            
            if veriyisifirla[0]==1:
                eski_veri=enkoder
                enkoder=enkoder-eski_veri
                veriyisifirla[0]=0
                hesapla[0]=1

            if hesapla[0]==1:
                enkoder=enkoder-eski_veri
       
            

            ilerlemeList[0]=predict_ileri(float(aci),float(enkoder),model_ileri_linear, model_ileri_poly)

            yonlenmeList[0]=predict_ileri(str(aci),str(enkoder),model_yanal_linear,model_yanal_poly)

            print(f"ilerleme miktarı: {ilerlemeList[0]}")
            print(f"yonlenme miktarı: {yonlenmeList[0]}")
            
            time.sleep(0.3)
        except:
            print('hata!!!!')
            continue

