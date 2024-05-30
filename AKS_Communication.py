
# BU KOD YAPAY ZEKA İŞLEMLERİ SONUCUNDA ARACIN KONTROL EDİLEBİLMESİ İÇİN YAZILMIŞTIR.
# ARAÇ KONTROL SİSTEMİNE BAĞLI OLAN STM KONTROLCÜSÜNE BELİRLİ KOMUTLAR GÖNDEREREK ARACI HAREKET ETTİRMEYİ SAĞLAR.

'''
 Usage example :
>>> import AKS_Communication as aks
>>> stm = aks.STM_Communication("COM10")
>>> stm.send_command(aks.Register.STEERING_ANGLE,20)

'''

import minimalmodbus
import time
from enum import Enum

class Register(Enum):
    STEERING_ANGLE = 0
    BRAKE = 1
    MOTOR_POWER = 2
    READ_WHEEL_ANGLE = 3
    READ_BRAKE_PRESSED = 4
    READ_BRAKE_RELEASED = 5
    READ_ODOMETER = 6
    REVERSE_COMMAND = 7
    LEFT_TURN_SIGNAL = 8
    RIGHT_TURN_SIGNAL = 9
    EMERGENCY_STOP = 10
    HEADLIGHTS_ON = 11
    MANUAL_DRIVE_MODE = 12
    RESET_ENCODER = 13
    GPS_LATITUDE = 14
    GPS_LONGITUDE = 15
    GPS_SPEED = 16
    GPS_ALTITUDE = 17
    GPS_ACTIVE = 18

class STM_Communication:
    def __init__(self, port, slave_address=1, baudrate=38400):
        self.instrument = minimalmodbus.Instrument(port, slave_address)
        self.instrument.serial.baudrate = baudrate
        # Port parametresine göre 'COMx' veya '/dev/ttyUSBx' gibi bir değer kullanabilirsiniz.
        # slave_address, STM mikrodenetleyicinizin Modbus adresidir.

    def send_command(self, num_of_registers, data):
        try:
            datatemp=data
            if data>-32769 and data<32768:
                if (data<0):
                    data = 65536 + data
                else:
                    pass
                self.instrument.write_register(num_of_registers.value, data, functioncode=6)
                print(f'{num_of_registers.name} degeri {datatemp} olarak gonderildi.')
            else:
                print("Fonksiyon icerisine 32767 ila -32768 araliginda deger giriniz.")

        except minimalmodbus.ModbusException as e:
            print(f"hata : {e}")
            pass

    def read_data(self,num_of_registers):
        # Belirli bir register adresinden veri okuma
        data = self.instrument.read_register(num_of_registers.value)
        return data

if __name__ == "__main__":

    stm=STM_Communication('COM10')
    stm.send_command(Register.BRAKE,1)
    print(stm.read_data(Register.READ_BRAKE_PRESSED))
