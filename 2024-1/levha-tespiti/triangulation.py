import numpy as np


def find_depth(right_point, left_point, frame_right, frame_left, baseline,f, alpha):

    # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]:
    height_right, width_right, depth_right = frame_right.shape
    # Sağ kamera görüntüsünün yüksekliğini, genişliğini ve derinliğini alırız. frame_right sağ kamera görüntüsünü temsil eder.

    
    height_left, width_left, depth_left = frame_left.shape
    # Sol kamera görüntüsünün yüksekliğini, genişliğini ve derinliğini alırız. frame_left sol kamera görüntüsünü temsil eder.

    if width_right == width_left:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)
        # Sağ ve sol kamera görüntülerinin genişlikleri aynı mı diye kontrol ederiz. Eğer aynıysa, odak uzunluğunu piksel cinsinden hesaplamak için gerekli işlemleri yaparız.

    else:
        print('Left and right camera frames do not have the same pixel width')
        # Eğer farklıysa, kullanıcıya uyarı verilir.


    x_right = right_point[0]
    x_left = left_point[0]
    # Sağ ve sol kameradan gelen nesne noktalarının yatay koordinatlarını alınır. 

    # CALCULATE THE DISPARITY:
    disparity = x_left-x_right      #Displacement between left and right frames [pixels]
    # Sağ ve sol kameradan alınan nesne noktalarının yatay koordinatları arasındaki farkı (disparity) hesaplarız.

    if disparity==0:
        zDepth=99999
        # Eğer disparity 0 ise, derinlik değeri hesaplanamayacağı için zDepth'i 99999 olarak ayarlarız. Aksi durumda, derinlik değerini hesaplarız.
    
    else:

        # CALCULATE DEPTH z:
        zDepth = (baseline*1000)/disparity     # Derinliğin cm cinsinden değeri hesaplanır.

    return zDepth
    # Hesaplanan derinlik değerini fonksiyonun sonucu olarak döndürürüz.
