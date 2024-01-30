import time
from enkoder.ardunio import write_read


def counter(wait_time):
    baslangic_zamani = time.time()

    while True:
        simdiki_zaman = time.time()
        gecen_vakit = simdiki_zaman - baslangic_zamani
        
        if gecen_vakit >= wait_time:
            break

def hareket_durak(enkoder_veriler,labellar,states,lidaretkin,goruntuislemeetkin):
    if lidaretkin[0]==0:
        goruntuislemeetkin[0]=1
        write_read('w0\n')
        #write_read('b1\n')
        #time.sleep(1) 
        write_read('t-65\n')
        #time.sleep(2) 
        
        enkoder_veriler[0][0] = 1
    
        enkoder_veriler[1][0]=0
        enkoder_veriler[2][0]=0
        
        enkoder_veriler[1][0]=1
        counter(2)
        
        #write_read('b0\n')
        #time.sleep(1) 
        write_read('w80\n')
        
        while enkoder_veriler[2][0] < 200:
            print("ENKODER VERILERI: ",enkoder_veriler[2][0])
            continue 
        
        write_read('w0\n')
        #write_read('b1\n')
        write_read('t99\n')
        enkoder_veriler[0][0] = 1
    
        enkoder_veriler[1][0]=0
        enkoder_veriler[2][0]=0
        
        enkoder_veriler[1][0]=1
        counter(2)

        #write_read('b0\n') 
        write_read('w80\n')
        while enkoder_veriler[2][0] < 210:
            continue 
        write_read('w0\n')
        #write_read('b1\n') 
        write_read('t0\n')
        time.sleep(32)
        
        write_read('t65\n')
        write_read('b0\n')
        enkoder_veriler[0][0] = 1
    
        enkoder_veriler[1][0]=0
        enkoder_veriler[2][0]=0
        
        enkoder_veriler[1][0]=1
        counter(2)
        write_read('w80\n') 

        while enkoder_veriler[2][0] < 200:
            continue
        write_read('w0\n') 
        #write_read('b1\n')
        #time.sleep(1)
        write_read('t-99\n')
        write_read('b0\n')
        
        enkoder_veriler[0][0] = 1
    
        enkoder_veriler[1][0]=0
        enkoder_veriler[2][0]=0
        
        enkoder_veriler[1][0]=1
        counter(2)
        write_read('w80\n') 
        while enkoder_veriler[2][0] < 210:
            continue
        write_read('w0\n') 
        #write_read('b1\n')
        write_read('t0\n')
        write_read('b0\n')
        write_read('w80\n') 
        goruntuislemeetkin[0]=0
    labellar['durak']==99999

