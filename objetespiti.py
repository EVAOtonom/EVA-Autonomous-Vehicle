import time
import cv2 as cv
import triangulation as tri
from karar_algoritması import karar


def uzaklikbelirle(customlabels, customcord,customclasses,custommodel,k,sagresim,solresim,labellar,states,enkoder_veriler,lidaretkin,goruntuislemeetkin):  
    x_shape = solresim.shape[1]
    y_shape = solresim.shape[0]
    
    for a in range(0,k):
    
        row = customcord[a]
        sınıf2=customclasses[int(customlabels[a])]

        if row[4]>0.4:
            x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
            boyut=(x2-x1)*(y2-y1)

            x=int((x1+x2)/2)
            y=int((y1+y2)/2)
            print("NESNE TESPITI YAPTIM ",str(sınıf2))
            solresim=cv.rectangle(solresim, (x1, y1), (x2, y2), (255,0,0), 2)
            solresim=cv.putText(solresim, sınıf2, (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)


            center_left=(x,y)
            img_pred=cv.cvtColor(sagresim,cv.COLOR_BGR2RGB)
            customresults2=custommodel(img_pred)
            customlabels2, customcord2 = customresults2.xyxyn[0][:, -1], customresults2.xyxyn[0][:, :-1]

            f=len(customlabels2)


            for b in range(0,f):
                
                row2 = customcord2[b]
                sınıf=customclasses[int(customlabels2[b])]
                if row2[4]>0.4: 
                    
                    x1, y1, x2, y2 = int(row2[0] * x_shape), int(row2[1] * y_shape), int(row2[2] * x_shape), int(row2[3] * y_shape)
                    boyut=(x2-x1)*(y2-y1)
                    x=int((x1+x2)/2)
                    y=int((y1+y2)/2)
                    print("NESNE TESPITI YAPTIM")
                    sagresim=cv.rectangle(sagresim, (x1, y1), (x2, y2), (255,0,0), 2)
                    sagresim=cv.putText(sagresim, sınıf, (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
                    
                    if boyut>0:
                        if sınıf==sınıf2:
                            center_right=(x,y)
                            depth = tri.find_depth(center_right, center_left, sagresim, solresim, 12, 1000, 88)
                            print("derinlik: ",depth)
                            if depth>0:
                                labellar[sınıf]=depth
                                
                                sagresim=cv.putText(sagresim, "Uzaklik: "+str(depth)+" cm", (x1, y1-50), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

                                karar(labellar,states,enkoder_veriler,lidaretkin,goruntuislemeetkin) 
                            
                            