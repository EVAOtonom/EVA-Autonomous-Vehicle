import time
import math
from enkoder.ardunio import write_read

def counter(wait_time):
    baslangic_zamani = time.time()

    while True:
        simdiki_zaman = time.time()
        gecen_vakit = simdiki_zaman - baslangic_zamani
        
        if gecen_vakit >= wait_time:
            break


def teknikKontrol(lidar,lidaretkin,enkoder_veriler,goruntuislemeetkin,ensol,ensag):
    try:
        while True:

            for scan in lidar.iter_measurments():
                #print(scan)
                
                if (int(scan[2])>345 and int(scan[2])<360):
                    if scan[3]<500:
                        print(scan[3])
                        continue
                    aci=int(scan[2])
                    print("LIDAR VERISI: ",scan[3],aci)
                    if scan[3]<2000 and scan[3]>500:
                        if goruntuislemeetkin[0]==0:
                                print("ENGELDEN KAC")
                                lidaretkin[0]=1
                                write_read("w0\n")
                                time.sleep(0.1)
                                #write_read("b1\n")
                                time.sleep(0.1)
                                write_read("t0\n")
                                enkoder_veriler[0][0] = 1
    
                                enkoder_veriler[1][0]=0
                                enkoder_veriler[2][0]=0
                                
                                enkoder_veriler[1][0]=1
                                time.sleep(0.1)
                                write_read("b0\n")
                                counter(2)
                                write_read("r\n")
                                time.sleep(0.1)
                                write_read("w80\n")
                                time.sleep(0.1)
                                while enkoder_veriler[2][0] > -200:
                                    continue 
                                write_read("w0\n")
                                time.sleep(0.1)
                                #write_read("b1\n")
                                counter(1)
                                write_read("r\n")
                                time.sleep(0.1)
                                if ensol==1:

                                    write_read("t90\n")
                                    time.sleep(0.1)
                                    enkoder_veriler[0][0] = 1
    
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    
                                    counter(2)
                                    
                                    write_read("b0\n") 
                                    time.sleep(1) 
                                    write_read("w80\n")
                                    time.sleep(0.1)
                                    while enkoder_veriler[2][0] < 225:
                                        continue 

                                    write_read('w0\n')
                                    time.sleep(0.1)
                                    #write_read('b1\n')
                                    time.sleep(0.1)
                                    write_read('t-99\n')
                                    time.sleep(0.1)
                                    enkoder_veriler[0][0] = 1
                                
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    counter(2)

                                    write_read('b0\n')
                                    time.sleep(0.1) 
                                    write_read('w80\n')
                                    time.sleep(0.1)
                                    while enkoder_veriler[2][0] < 250:
                                        continue 
                                elif ensag==1:
                                    write_read('t-90\n')
                                    time.sleep(2) 
                                    
                                    enkoder_veriler[0][0] = 1
                                
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    counter(2)
                                    
                                    write_read('b0\n')
                                    time.sleep(1) 
                                    write_read('w80\n')
                                    time.sleep(0.1)
                                    while enkoder_veriler[2][0] < 225:
                                        continue 
                                    
                                    write_read('w0\n')
                                    time.sleep(0.1)
                                    #write_read('b1\n')
                                    time.sleep(0.1)
                                    write_read('t99\n')
                                    time.sleep(0.1)
                                    enkoder_veriler[0][0] = 1
                                
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    counter(2)

                                    write_read('b0\n')
                                    time.sleep(0.1) 
                                    write_read('w80\n')
                                    while enkoder_veriler[2][0] < 250:
                                        continue 
                                else:
                                    write_read("t90\n")
                                    time.sleep(0.1)
                                    enkoder_veriler[0][0] = 1
    
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    
                                    counter(2)
                                    
                                    write_read("b0\n")
                                    time.sleep(1)
                                    write_read("w80\n")
                                    time.sleep(0.1)
                                    while enkoder_veriler[2][0] < 225:
                                        continue 

                                    write_read('w0\n')
                                    time.sleep(0.1)
                                    #write_read('b1\n')
                                    time.sleep(0.1)
                                    write_read('t-99\n')
                                    time.sleep(0.1)
                                    enkoder_veriler[0][0] = 1
                                
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    counter(2)

                                    write_read('b0\n')
                                    time.sleep(0.1) 
                                    write_read('w80\n')
                                    time.sleep(0.1)
                                    while enkoder_veriler[2][0] < 250:
                                        continue 
                                write_read('w0\n') 
                                time.sleep(0.1)
                                #write_read('b1\n')
                                time.sleep(0.1)
                                write_read('t0\n')
                                time.sleep(1)
                                write_read('b0\n')
                                time.sleep(0.1)
                                write_read('w80\n')
                                time.sleep(0.1) 

                                lidaretkin[0]=0
                        print("DURDUM  {} : ".format(scan[3]))

                if (int(scan[2])>0 and int(scan[2])<25):
                    if scan[3]<500:
                        continue
                    aci=int(scan[2])
                    print("LIDAR VERISI: ",scan[3],aci)
                    if scan[3]<2000 and scan[3]>500:
                        if goruntuislemeetkin[0]==0:
                                print("ENGELDEN KAC")
                                lidaretkin[0]=1
                                write_read("w0\n")
                                time.sleep(0.1)
                                #write_read("b1\n")
                                time.sleep(0.1)
                                write_read("t0\n")
                                enkoder_veriler[0][0] = 1
    
                                enkoder_veriler[1][0]=0
                                enkoder_veriler[2][0]=0
                                
                                enkoder_veriler[1][0]=1
                                time.sleep(0.1)
                                write_read("b0\n")
                                counter(2)
                                write_read("r\n")
                                time.sleep(0.1)
                                write_read("w80\n")
                                time.sleep(0.1)
                                while enkoder_veriler[2][0] > -200:
                                    continue 
                                write_read("w0\n")
                                time.sleep(0.1)
                                #write_read("b1\n")
                                counter(1)
                                write_read("r\n")
                                time.sleep(0.1)
                                if ensol==1:

                                    write_read("t90\n")
                                    time.sleep(0.1)
                                    enkoder_veriler[0][0] = 1
    
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    
                                    counter(2)
                                    
                                    write_read("b0\n") 
                                    time.sleep(1) 
                                    write_read("w80\n")
                                    time.sleep(0.1)
                                    while enkoder_veriler[2][0] < 225:
                                        continue 

                                    write_read('w0\n')
                                    time.sleep(0.1)
                                    #write_read('b1\n')
                                    time.sleep(0.1)
                                    write_read('t-99\n')
                                    time.sleep(0.1)
                                    enkoder_veriler[0][0] = 1
                                
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    counter(2)

                                    write_read('b0\n')
                                    time.sleep(0.1) 
                                    write_read('w80\n')
                                    time.sleep(0.1)
                                    while enkoder_veriler[2][0] < 250:
                                        continue 
                                elif ensag==1:
                                    write_read('t-90\n')
                                    time.sleep(2) 
                                    
                                    enkoder_veriler[0][0] = 1
                                
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    counter(2)
                                    
                                    write_read('b0\n')
                                    time.sleep(1) 
                                    write_read('w80\n')
                                    time.sleep(0.1)
                                    while enkoder_veriler[2][0] < 225:
                                        continue 
                                    
                                    write_read('w0\n')
                                    time.sleep(0.1)
                                    #write_read('b1\n')
                                    time.sleep(0.1)
                                    write_read('t99\n')
                                    time.sleep(0.1)
                                    enkoder_veriler[0][0] = 1
                                
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    counter(2)

                                    write_read('b0\n')
                                    time.sleep(0.1) 
                                    write_read('w80\n')
                                    while enkoder_veriler[2][0] < 250:
                                        continue 
                                else:
                                    write_read("t90\n")
                                    time.sleep(0.1)
                                    enkoder_veriler[0][0] = 1
    
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    
                                    counter(2)
                                    
                                    write_read("b0\n")
                                    time.sleep(1)
                                    write_read("w80\n")
                                    time.sleep(0.1)
                                    while enkoder_veriler[2][0] < 225:
                                        continue 

                                    write_read('w0\n')
                                    time.sleep(0.1)
                                    #write_read('b1\n')
                                    time.sleep(0.1)
                                    write_read('t-99\n')
                                    time.sleep(0.1)
                                    enkoder_veriler[0][0] = 1
                                
                                    enkoder_veriler[1][0]=0
                                    enkoder_veriler[2][0]=0
                                    
                                    enkoder_veriler[1][0]=1
                                    counter(2)

                                    write_read('b0\n')
                                    time.sleep(0.1) 
                                    write_read('w80\n')
                                    time.sleep(0.1)
                                    while enkoder_veriler[2][0] < 250:
                                        continue 
                                write_read('w0\n') 
                                time.sleep(0.1)
                                #write_read('b1\n')
                                time.sleep(0.1)
                                write_read('t0\n')
                                time.sleep(1)
                                write_read('b0\n')
                                time.sleep(0.1)
                                write_read('w80\n')
                                time.sleep(0.1) 

                                lidaretkin[0]=0
                        print("DURDUM  {} : ".format(scan[3]))

                
    except KeyboardInterrupt:
        print("Stopping")
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        teknikKontrol()

