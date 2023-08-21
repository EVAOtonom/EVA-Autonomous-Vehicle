import time
from ardunio import sendToArduino

def counter(wait_time):
    baslangic_zamani = time.time()

    while True:
        simdiki_zaman = time.time()
        gecen_vakit = simdiki_zaman - baslangic_zamani
        if gecen_vakit >= wait_time:
            break

def karar(labellar,states):

    if labellar['sag']<900:
        if states['aracdurdu'] == False:
            print("ARAC SAGA DONUYOR")
            sendToArduino('w0\n') #hızı sıfırla
            counter(1)
            sendToArduino('t-30') #t açı komutunu gönderir arduinoya, -30, 30 derece sağa döndürür tekeri
            counter(1)
            sendToArduino('w90\n') #w hız komutunu gönderir, hızı 90 olarak ayarlıyoruz burada
            counter(1)
            sendToArduino('w0\n') #hızı sıfırla, aracın hızını kesiyoruz yani
            counter(1)
            sendToArduino('t0') #tekerin açısını sıfır yap yani tekeri düzelt
            labellar['sag']==999999
            states['aracdurdu'] = True
        print('saga donus islemi tamam')

    if labellar['soladonulmez']<800:
        if states['aracdurdu'] == False:
            print("ARAC SAGA DONUYOR")
            sendToArduino('w0\n')
            counter(1)
            sendToArduino('w90\n')
            counter(1)
            sendToArduino('w0\n')
            counter(1)
            labellar['soladonulmez'] = 999999
            states['aracdurdu'] = True
        print('sola donemedi')
    
