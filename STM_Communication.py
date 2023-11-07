import minimalmodbus
#slaveadress = 1 -> STM'in kaçıncı slave olduğunu belirtir.
#register_adress = 0 -> Direksiyon açısı komutu göndermeyi sağlar.
instrument = minimalmodbus.Instrument('COM4',slaveaddress=1) 
instrument.serial.baudrate = 38400

def send_to_STM(register_adress,data):
    write_register_address=register_adress
    value=data
    instrument.write_register(write_register_address, value, functioncode=6)  # Function code 6: Write Single Register
    print(f'Register {write_register_address} değeri {data} olarak yazıldı.')
