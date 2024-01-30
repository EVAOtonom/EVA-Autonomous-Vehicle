import serial


import time

import csv

import keyboard
import pickle

"""
import sklearn
from enkoder.ilerleme import predict_ileri
from enkoder.ilerleme import predict_yonlendirme"""
"""

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)
"""
arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)

time.sleep(2)

"""
model_ileri_linear = pickle.load(open("enkoder\\ilerlemeLinear4.pickle","rb"))
model_ileri_poly = pickle.load(open("enkoder\\ilerlemePoly4.pickle","rb"))

model_yanal_linear = pickle.load(open("enkoder\\yonlenmeLinear4.pickle","rb"))
model_yanal_poly = pickle.load(open("enkoder\\yonlenmePoly4.pickle","rb"))

"""
def write_read(x):
    #print("ardunioya veri göndermeye çalıştım")
    arduino.write(x.encode())
    time.sleep(0.1)
    #print("ardunioya veri gönderdim")



def readAciEnkoder():
    while True:
        try:
            
            data=arduino.readline()
                
            data=str(data)
            
            data=data.replace("b'","")
            data=data.replace("\\n'","")
            print(data)
            enkoder = data.split(',')[0]
            
            enkoder=float(enkoder)*0.1477
 
            #enkoder_son_veri=mesafe

            """         
           if enkoder_son_veri !=0:
                hiz=enkoder_son_veri-enkoder_eski_veri/0.3
                
                enkoder_eski_veri=enkoder_son_veri
                hizlar.append(hiz)
                if hiz==10:
                    with open('hiz_veri.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
            """
            
            aci = data.split(',')[1]
            print("aci:   ",aci)
            print("Mesafe   ",enkoder)
            return aci,enkoder

    
        except:
            print('hata!!!!')
            continue


def read(enkoderList,veriyisifirla,hesapla):
    
    global model_ileri_linear, model_ileri_poly,model_yanal_linear,model_yanal_poly
    enkoder_son_veri=0
    enkoder_eski_veri=0
    hizlar=[]
    while True:
        try:
            
            aci,enkoder=readAciEnkoder()
            
            if veriyisifirla[0]==1:
                eski_veri=enkoder
                enkoder=enkoder-eski_veri
                veriyisifirla[0]=0
                hesapla[0]=1
                enkoderList[0] = 0 

            if hesapla[0]==1:
                enkoder=enkoder-eski_veri
                
            enkoderList[0] = float(enkoder) 
            print(enkoderList)
 
        except:
            #print('hata!!!!')
            continue
