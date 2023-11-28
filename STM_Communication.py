import minimalmodbus

#32767 ile -32768 aralığında değer gönderilebilir. Fonksiyon içerisine 32767 ila -32768 aralığında değer giriniz.

#slaveadress = 1 ->     STM'in kaçıncı slave olduğunu belirtir. Tek STM kullandığımız için 1 olmalı.
#functioncode=6  ->     Write Single Register
#register_adress = 0 -> Direksiyon açısı komutu göndermeyi sağlar.
#register_adress = 1 -> Fren komutu göndermeyi sağlar. 1 frene basar 0 freni salar.
#register_adress = 2 -> Motora komut göndermeyi sağlar.

instrument = minimalmodbus.Instrument('COM7',slaveaddress=1) 
instrument.serial.baudrate = 38400

def send_to_STM(register_adress,data):
    if data>-32769 and data<32768:
        write_register_address=register_adress
        if (data<0):
            data = 65536 + data
        else:
            pass
        value=data
        instrument.write_register(write_register_address, value, functioncode=6)
        print(f'Register {write_register_address} değeri {data} olarak yazıldı.')
    else:
        print("Fonksiyon içerisine 32767 ila -32768 aralığında değer giriniz.")

send_to_STM(0,1000)
