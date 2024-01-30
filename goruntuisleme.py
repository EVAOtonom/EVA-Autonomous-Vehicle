import torch
import cv2 as cv
import pyzed.sl as sl
import sys
from threading import Thread, Lock
from objetespiti import uzaklikbelirle



kilid=1

#resim ureten thread fonksiyonunun tanımı
def kamera(lock,zed,sl,init):
    global kilid,img_sol,img_lane,img_sag



    while True:

        # Create and set RuntimeParameters after opening the camera
        runtime_parameters = sl.RuntimeParameters()
        runtime_parameters.sensing_mode = sl.SENSING_MODE.STANDARD  # Use STANDARD sensing mode
        # Setting the depth confidence parameters
        runtime_parameters.confidence_threshold = 100
        runtime_parameters.textureness_confidence_threshold = 100

        image = sl.Mat()
        depth = sl.Mat()
        point_cloud = sl.Mat()
        imagesag = sl.Mat()
        mirror_ref = sl.Transform()
        mirror_ref.set_translation(sl.Translation(2.75,4.0,0))
        tr_np = mirror_ref.m

        err = zed.grab(runtime_parameters)

        # Retrieve left image
        zed.retrieve_image(image, sl.VIEW.LEFT)
        img_sol = image.get_data()

        zed.retrieve_image(imagesag, sl.VIEW.RIGHT)
        img_sag=imagesag.get_data()
        
        # Retrieve depth map. Depth is aligned on the left image
        #zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
        # Retrieve colored point cloud. Point cloud is aligned on the left image.
        zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
        kilid=0
        
            
        while kilid==0:
            with lock:
                cv.imshow("Obje Tespiti sol",img_sol)
                cv.imshow("Obje Tespiti sag",img_sag)
                
            
            if kilid==1:
                with lock:
                    cv.imshow("Obje Tespiti sol",img_sol)
                    cv.imshow("Obje Tespiti sag",img_sag)
                    cv.waitKey(1)




        if kilid==1:
            with lock:
                cv.imshow("Obje Tespiti sol",img_sol)
                cv.imshow("Obje Tespiti sag",img_sag)
                cv.waitKey(1)







def goruntuisleme(sl,zed,custommodel,customclasses,labellar,states,enkoder_veriler,goruntuislemeetkin,lidaretkin,ensol,ensag,init):
    global kilid,img_sol,img_lane,img_sag

    lock_main=Lock()
    lock_cam=Lock()
    thread_cam = Thread(target=kamera, args=(lock_cam,zed,sl,init,))
    thread_cam.start()

    while True:

        while lidaretkin[0]==1:
            pass

        if kilid==0:
            sagresim=img_sag.copy()
            solresim = img_sol.copy()

            img_pred=cv.cvtColor(solresim,cv.COLOR_BGR2RGB)
            customresults=custommodel(img_pred)
            print("obje tespiti yapıldı")
            customlabels, customcord = customresults.xyxyn[0][:, -1], customresults.xyxyn[0][:, :-1]
            k=len(customlabels)

            if k>0:
                
                uzaklikbelirle(customlabels, customcord,customclasses,custommodel,k,sagresim,solresim,labellar,states,enkoder_veriler,lidaretkin,goruntuislemeetkin)


            k=0


            with lock_main:
                img_sol=solresim.copy()
                img_sag=sagresim.copy()
                kilid=1
                
