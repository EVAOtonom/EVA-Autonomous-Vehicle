import time
import cv2 as cv
import triangulation as tri

def goruntuisleme(customlabels, customcord, confidence, class_names, custommodel,k,sagresim,solresim,labellar):  
    x_shape = solresim.shape[1]
    y_shape = solresim.shape[0]
    
    for a in range(0,k):
    
        row = customcord
        # row = (x1, y1, x2, y2, confidence)  
        sınıf2=customlabels

        if confidence>0.7:
            x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])
            boyut=(x2-x1)*(y2-y1)

            x=int((x1+x2)/2)
            y=int((y1+y2)/2)
            print("NESNE TESPITI YAPTIM ",str(sınıf2))
            solresim=cv.rectangle(solresim, (x1, y1), (x2, y2), (255,0,0), 2)
            solresim=cv.putText(solresim, sınıf2, (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
            

            center_left=(x,y)
            img_pred=cv.cvtColor(sagresim,cv.COLOR_BGR2RGB)
            results2=custommodel(img_pred)
            print("obje tespiti yapıldı")
            for r in results2:
                boxes = r.boxes
                for box in boxes:
                    model_output_class2 = class_names [int(box.cls[0])] #yalnız bir levhayı algılar
                    model_output_boundingbox2 = box.xyxy[0]
                    model_output_confidence2 = box.conf[0]
                    f=len(boxes)


                    for b in range(0,f):
                        
                        row2 = model_output_boundingbox2
                        sınıf=model_output_class2
                        # İç döngüde tespit edilen nesnenin bilgileri (row2) alınıyor ve sınıf adı (sınıf) customclasses sözlüğünden alınıyor.
                        
                        if model_output_confidence2>0.7: 
                            
                            x1, y1, x2, y2 = int(row2[0] * x_shape), int(row2[1] * y_shape), int(row2[2] * x_shape), int(row2[3] * y_shape)
                            boyut=(x2-x1)*(y2-y1)
                            x=int((x1+x2)/2)
                            y=int((y1+y2)/2)
                            # Tespit edilen nesnenin koordinatları ölçeklenir ve merkez koordinatları x ve y hesaplanır.
                            print("NESNE TESPITI YAPTIM")
                            sagresim=cv.rectangle(sagresim, (x1, y1), (x2, y2), (255,0,0), 2)
                            sagresim=cv.putText(sagresim, sınıf, (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
                            
                            if boyut>0:
                                if sınıf==sınıf2: # Eğer nesne, solresim'deki daha önce tespit edilen nesneyle aynı sınıftaysa, triangulasyon işlemi için kullanılan tri.find_depth fonksiyonu çağrılır.
                                    center_right=(x,y)
                                    depth = tri.find_depth(center_right, center_left, sagresim, solresim, 12, 1000, 88)
                                    # triangulation dosyasının içinden aldığımız find_depth fonksiyonu derinlik verisini bulmamızı sağlar. 
                                    # Yukarıda triangulation dosyasını tri şeklinde import ettiğimiz için burada o dosyanın içindeki fonksiyonu tri.find_depth şeklinde belirttik.
                                    print("@@@@@@@@@@@DERINLIK: ",depth)
                                    labellar[sınıf]=depth
                                    #her label için yani tespit edilen her nesnenin derinlik değerini bulabilmek için bunu yazdık
                                    
                                    solresim=cv.putText(solresim, "Uzaklık: "+str(depth)+" cm", (x1, y1-30), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
