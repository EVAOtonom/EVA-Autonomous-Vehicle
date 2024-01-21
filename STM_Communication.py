import minimalmodbus

# BU KOD YAPAY ZEKA İŞLEMLERİ SONUCUNDA ARACIN KONTROL EDİLEBİLMESİ İÇİN YAZILMIŞTIR.
# ARAÇ KONTROL SİSTEMİNE BAĞLI OLAN STM KONTROLCÜSÜNE BELİRLİ KOMUTLAR GÖNDEREREK ARACI HAREKET ETTİRMEYİ SAĞLAR.

#register_adress = 0 -> Araca direksiyon açısı vermeyi sağlar. -40 ile 40 aralığında değer göndermelisiniz.
#register_adress = 1 -> Araca fren yaptırmayı sağlar. 1 gönderirseniz fren yapar, 0 gönderirseniz freni bırakır.
#register_adress = 2 -> Araca motor gücü vermeyi sağlar. 2 ile 10 aralığında değer göndermelisiniz. Genel olarak 2 yeterli.
#register_adress = 3 -> Anlık tekerlek açısını okumayı sağlar.
#register_adress = 4 -> Fren durumunun basılı olduğunu okumayı sağlar.
#register_adress = 5 -> Fren durumunun basılı olmadığını okumayı sağlar.
#register_adress = 6 -> Gidilen mesafenin öğrenilmesini sağlar. (Arka enkoder aracılığıyla)
#register_adress = 7 -> Geri vites komutu göndermeyi sağlar. 1 Göndermelisiniz.
#register_adress = 8 -> Sola sinyal vermeyi sağlar. 1 Göndermelisiniz.
#register_adress = 9 -> Sağa sinyal vermeyi sağlar. 1 Göndermelisiniz.
#register_adress = 10 -> Acil stop yapmayı sağlar.  1 Göndermelisiniz.
#register_adress = 11 -> Ön farların açılmasını sağlar. 1 Göndermelisiniz.
#register_adress = 12 -> Aracın manuel sürüş moduna geçmesini sağlar.

instrument = minimalmodbus.Instrument('COM10',slaveaddress=1) 
instrument.serial.baudrate = 38400

def send_to_STM(register_adress,data):
    try:
        datatemp=data
        if data>-32769 and data<32768:
            write_register_address=register_adress
            if (data<0):
                data = 65536 + data
            else:
                pass
            instrument.write_register(write_register_address, data, functioncode=6)
            print(f'Register {write_register_address} değeri {datatemp} olarak yazıldı.')
        else:
            print("Fonksiyon içerisine 32767 ila -32768 aralığında değer giriniz.")
    except minimalmodbus.ModbusException as e:
        print(f"hata : {e}")
        pass

if __name__ == "__main__":

    send_to_STM(0,20)
    #instrument.read_register(10)
