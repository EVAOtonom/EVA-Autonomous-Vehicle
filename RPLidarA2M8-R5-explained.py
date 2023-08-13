from rplidar import RPLidar #rplidar kütüphanesinden RPLidar sınıfını çekiyoruz
import time #lidarın başlatılması için gerekli zaman aşımını verebilmek için time kütüphanesini çekiyoruz.

#Bilgisayarımıza CP2102 USB to UART Bridge Controller Driver'ını yükledikten sonra Aygıt Yöneticisinden lidarımızın com portunu öğrenip port_name değişkenine atıyoruz
PORT_NAME = 'COM3' 
#UART Bridge üzerinde işaretli olan BAUDRATE değerini değişkene atıyoruz. Baud Rate: Saniyede gönderilecek bit sayısını belirtir.
BAUD_RATE = 115200

#lidar isminde bir RPLidar sınıfı oluşturuyoruz ve bu sınıfın içine gerekli değişkenleri gönderiyoruz.
lidar = RPLidar(PORT_NAME,baudrate=BAUD_RATE)

def runLidar():
    try:
        print('LIDAR Baslatiliyor.\nDurdurmak için \'CTRL+C\'')
        time.sleep(2)
        for data in lidar.iter_scans():
            for q,angle,distance in data:
                if angle>=350 or angle<=10:
                    print(distance)
    except KeyboardInterrupt:
        print('LIDAR Durduruluyor.')
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
#Oluşturduğumuz fonksiyon içerisinde lidarı istediğimizde durdurabilmek için try-except bloğu oluşturuyoruz.
#Lidar sınıfımız içerisinde mevcut olan iter_scans() fonksiyonunu çalıştırıyoruz.
#Fonksiyonun bize verdiği lazer gücü, açı ve mesafe değerlerini veriler değişkeni içerisine atıyoruz.
#Son olarak işleyeceğimiz aralıktaki açı değerlerinden gelen mesafe verisini yazdırıyoruz.
runLidar()