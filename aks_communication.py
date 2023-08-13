import serial
import time

#AKS Kartı tanımlanıyor. Burada timeout değeri arduinodan gelen veri 0.1 saniyede gelmezse iletişimi kesmesi içindir.
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)
time.sleep(2)

def sendToArduino(x):
    arduino.write(x.encode())
    time.sleep(0.1)
    #Seri haberleşmede gönderilecek veriyi uygun formata çevirmek gerekir.
    #Bunun için encode() fonksiyonu kullanılır. Bu sayede 8 bitlik dizilere (UTF-8) çevrilir. 
    #Karşı taraf aldığında ise decode() şeklinde tekrar metin haline çevirir.