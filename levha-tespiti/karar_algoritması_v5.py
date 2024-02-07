import time
from enkoder.ardunio import write_read

from enkoder.ardunio import read
#from OTONOM2023_TEST_KODLARI.goruntuisleme.triangulation import find_depth
from karar_ver import hareket_durak


def counter(wait_time):
    baslangic_zamani = time.time()

    while True:
        simdiki_zaman = time.time()
        gecen_vakit = simdiki_zaman - baslangic_zamani
        
        if gecen_vakit >= wait_time:
            break

def turn_and_wait(angle, time_to_wait):
    write_read('t' + str(angle) + '\n')
    time.sleep(time_to_wait)
    if angle < 0:
        print("sağa dön")
    else:
        print("sola dön")
    time.sleep(time_to_wait)


def karar(labellar,states,enkoder_veriler,lidaretkin,goruntuislemeetkin):

    confidence_label=max(labellar, key=lambda key:labellar[key])
    confidence_value=labellar[confidence_label]

    if confidence_label== "kirmizi" and confidence_value>=0.75:
        print("ARAC DURDU")
        if states['aracdurdu']==False:
            write_read('w0\n')
            #write_read('b1\n')
            states['aracdurdu']=True
            labellar['kirmizi']==999999
           
    if confidence_label== "yesil" and confidence_value>=0.80:
        print("ARAC GIDIYOR")
        if states['aracdurdu']==True:
            write_read('b0\n')
            write_read('w80\n')
            states['aracdurdu']=False
            labellar['yesil']==99999
        
    """   
    if confidence_label== "dur" and confidence_value>=0.85:
        if states['aracdurdu']==False:
            write_read('w0\n')
            write_read('b1\n')
            print('arac beklemede')
    """

    if confidence_label== "sag" and confidence_value>=0.7:   #degistirilecek.
        print("ARAC SAGA DONUYOR")
        
        if lidaretkin[0]==0:
            enkoder_veriler[0][0] = 1
            enkoder_veriler[1][0]=0
            enkoder_veriler[2][0]=0
        
            enkoder_veriler[1][0]=1
            counter(2)
            while enkoder_veriler[2][0] < 450:   #degistirilecek
                continue 
            goruntuislemeetkin[0]=1
            write_read('t-95\n')
            enkoder_veriler[0][0] = 1
    
            enkoder_veriler[1][0]=0
            enkoder_veriler[2][0]=0
            
            enkoder_veriler[1][0]=1
            counter(2)
            while enkoder_veriler[2][0] < 430:    #degistirilecek
                continue 
            write_read("t0\n")
        for i in labellar:
            labellar[i]=9999

    if confidence_label== "sol" and confidence_value>=0.7:    #degistirilecek
        print("ARAC SOLA DONUYOR")
        
        if lidaretkin[0]==0:
            enkoder_veriler[0][0] = 1
            enkoder_veriler[1][0]=0
            enkoder_veriler[2][0]=0
        
            enkoder_veriler[1][0]=1
            counter(2)
            while enkoder_veriler[2][0] < 450:   #degistirilecek
                continue 
            goruntuislemeetkin[0]=1
            write_read('t95\n')
            enkoder_veriler[0][0] = 1
    
            enkoder_veriler[1][0]=0
            enkoder_veriler[2][0]=0
            
            enkoder_veriler[1][0]=1
            counter(2)
            while enkoder_veriler[2][0] < 400:    #degistirilecek
                continue 
            write_read("t0\n")
            for i in labellar:
                labellar[i]=9999


    if (confidence_label== "sag" and confidence_value>=0.7) or (confidence_label== "sol" and confidence_value>=0.7):      #degistirilecek
        print(confidence_label)
        if confidence_label== "girisyok" and confidence_value>=0.82:
            if confidence_label== "sagadonulmez" and confidence_value>=0.7:       #degistirilecek

                print("ARAC SOLA DONUYOR")
                
                if lidaretkin[0]==0:

                    enkoder_veriler[0][0] = 1
                    enkoder_veriler[1][0]=0
                    enkoder_veriler[2][0]=0
                
                    enkoder_veriler[1][0]=1
                    counter(2)
                    while enkoder_veriler[2][0] < 450:    #degistirilecek
                        continue 
                    goruntuislemeetkin[0]=1
                    write_read('t95\n')
                    enkoder_veriler[0][0] = 1
            
                    enkoder_veriler[1][0]=0
                    enkoder_veriler[2][0]=0
                    
                    enkoder_veriler[1][0]=1
                    counter(2)
                    while enkoder_veriler[2][0] < 400:     #degistirilecek
                        continue 
                    write_read("t0\n")
                
            elif confidence_label== "soladonulmez" and confidence_value>=0.7:     #degistirilecek
                print("ARAC SAGA DONUYOR")
                
                if lidaretkin[0]==0:
                    enkoder_veriler[0][0] = 1
                    enkoder_veriler[1][0]=0
                    enkoder_veriler[2][0]=0
                
                    enkoder_veriler[1][0]=1
                    counter(2)
                    while enkoder_veriler[2][0] < 450:     #degistirilecek
                        continue 
                    goruntuislemeetkin[0]=1
                    write_read('t-95\n')
                    enkoder_veriler[0][0] = 1
            
                    enkoder_veriler[1][0]=0
                    enkoder_veriler[2][0]=0
                    
                    enkoder_veriler[1][0]=1
                    counter(2)
                    while enkoder_veriler[2][0] < 400:     #degistirilecek
                        continue 
                    write_read("t0\n")
            else:
                print('Sola donuyor')
                
                if lidaretkin[0]==0:

                    enkoder_veriler[0][0] = 1
                    enkoder_veriler[1][0]=0
                    enkoder_veriler[2][0]=0
                
                    enkoder_veriler[1][0]=1
                    counter(2)
                    while enkoder_veriler[2][0] < 450:      #degistirilecek
                        continue 
                    goruntuislemeetkin[0]=1
                    write_read('t95\n')
                    enkoder_veriler[0][0] = 1
            
                    enkoder_veriler[1][0]=0
                    enkoder_veriler[2][0]=0
                    
                    enkoder_veriler[1][0]=1
                    counter(2)
                    while enkoder_veriler[2][0] < 400:       #degistirilecek
                        continue 
                    write_read("t0\n")
            for i in labellar:
                labellar[i]=9999
                

            
    """
    if confidence_label== "park" and confidence_value>=0.82:
        time.sleep(1)  

        if states['aracdurdu']==False:     

            turn_and_wait(-65, 4)
            write_read('w0\n')
            write_read('b1\n')
            time.sleep(1)
            turn_and_wait(65,1)
            write_read('b0\n')
            write_read('w65\n')
            turn_and_wait(65,4)
            write_read('w0\n')
            write_read('b1\n')
            turn_and_wait(0,32)
            print('arac beklemede')
            write_read('b0\n')
            time.sleep(1) 
            write_read('w65\n')
            turn_and_wait(45, 3) 
            turn_and_wait(-45, 3) 
            states['aracdurdu']=True
            labellar['park']==99999
    """

    
    if confidence_label== "durak" and confidence_value>=0.90: 
        hareket_durak(enkoder_veriler,labellar,states,lidaretkin,goruntuislemeetkin)
        for i in labellar:
            labellar[i]=9999
        
    goruntuislemeetkin[0]=0
