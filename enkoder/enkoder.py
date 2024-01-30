import keyboard
from ardunio import write_read
import time

from threading import Thread, Lock

from ardunio import read

enkoderList=[0]
veriyisifirla=[0]
hesapla=[0]
thread_enkoder=Thread(target=read,args=(enkoderList,veriyisifirla,hesapla))
thread_enkoder.start()


def kumanda():
    write_read("b1\n")
    aci=0
    write_read("t0\n")
    gerivitestemi=0
    frenbasık=1
    gazbasilimi=0
    
    while not(keyboard.is_pressed("esc")):
        time.sleep(0.01)
        if keyboard.is_pressed("w"):
            if gerivitestemi==1:
                write_read("b1\n")
                time.sleep(1)
                write_read("f\n")
                time.sleep(0.5)

                write_read("w70\n")
                gerivitestemi=0

            if frenbasık==1:
                write_read("b0\n")
                time.sleep(1)
                frenbasık=0
                write_read("f\n")
                time.sleep(0.1)
                write_read("w70\n")
                time.sleep(0.1)
            if gazbasilimi==0:
                write_read("w70\n")
                gazbasilimi=1
                
        if keyboard.is_pressed("a"):
            if frenbasık==1:
                write_read("b0\n")
                time.sleep(1)
                frenbasık=0

            if aci<90:
                aci=aci+5
                donmeacisi="t"+str(aci)+"\n"
                print("Acı:  ",aci)
                write_read(donmeacisi)

        if keyboard.is_pressed("d"):

            if frenbasık==1:
                write_read("b0\n")
                time.sleep(1)
                frenbasık=0

            if aci>-100:

                aci=aci-5
                donmeacisi="t"+str(aci)+"\n"
                print("Acı:  ",aci)
                write_read(donmeacisi)
            else:
                pass
        if keyboard.is_pressed("s"):
            time.sleep(0.5)
            if gerivitestemi==0:
                gerivitestemi==1
                time.sleep(0.1)
                write_read("w0\n")
                time.sleep(0.1)
                write_read("b1\n")
                time.sleep(0.1)
                write_read("r\n")
                time.sleep(0.1)
                write_read("b0\n")
                time.sleep(1)
                write_read("w70\n")
            else:
                if frenbasık==1:
                    write_read("b0\n")
                    time.sleep(1)
                    frenbasık=0
        if keyboard.is_pressed('space'):
            if frenbasık==0:
                write_read("w0\n")
                write_read("b1\n")
                time.sleep(0.1)
                frenbasık=1
                
        if keyboard.is_pressed('space'):
            if frenbasık==1:
                write_read("w0\n")
                write_read("b0\n")
                time.sleep(1)
                frenbasık=0
        
kumanda()


