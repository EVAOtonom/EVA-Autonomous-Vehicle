;; Auto-generated. Do not edit!


(when (boundp 'evaotonom::Sign)
  (if (not (find-package "EVAOTONOM"))
    (make-package "EVAOTONOM"))
  (shadow 'Sign (find-package "EVAOTONOM")))
(unless (find-package "EVAOTONOM::SIGN")
  (make-package "EVAOTONOM::SIGN"))

(in-package "ROS")
;;//! \htmlinclude Sign.msg.html


(defclass evaotonom::Sign
  :super ros::object
  :slots (_sign_index _depth ))

(defmethod evaotonom::Sign
  (:init
   (&key
    ((:sign_index __sign_index) 0)
    ((:depth __depth) 0.0)
    )
   (send-super :init)
   (setq _sign_index (round __sign_index))
   (setq _depth (float __depth))
   self)
  (:sign_index
   (&optional __sign_index)
   (if __sign_index (setq _sign_index __sign_index)) _sign_index)
  (:depth
   (&optional __depth)
   (if __depth (setq _depth __depth)) _depth)
  (:serialization-length
   ()
   (+
    ;; int8 _sign_index
    1
    ;; float32 _depth
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int8 _sign_index
       (write-byte _sign_index s)
     ;; float32 _depth
       (sys::poke _depth (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int8 _sign_index
     (setq _sign_index (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _sign_index 127) (setq _sign_index (- _sign_index 256)))
   ;; float32 _depth
     (setq _depth (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get evaotonom::Sign :md5sum-) "9d6f7ebc229c76b7f8002caeee511826")
(setf (get evaotonom::Sign :datatype-) "evaotonom/Sign")
(setf (get evaotonom::Sign :definition-)
      "int8 sign_index
float32 depth

")



(provide :evaotonom/Sign "9d6f7ebc229c76b7f8002caeee511826")


