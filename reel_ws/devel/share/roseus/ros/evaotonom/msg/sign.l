;; Auto-generated. Do not edit!


(when (boundp 'evaotonom::sign)
  (if (not (find-package "EVAOTONOM"))
    (make-package "EVAOTONOM"))
  (shadow 'sign (find-package "EVAOTONOM")))
(unless (find-package "EVAOTONOM::SIGN")
  (make-package "EVAOTONOM::SIGN"))

(in-package "ROS")
;;//! \htmlinclude sign.msg.html


(defclass evaotonom::sign
  :super ros::object
  :slots (_integer_value _float_value ))

(defmethod evaotonom::sign
  (:init
   (&key
    ((:integer_value __integer_value) 0)
    ((:float_value __float_value) 0.0)
    )
   (send-super :init)
   (setq _integer_value (round __integer_value))
   (setq _float_value (float __float_value))
   self)
  (:integer_value
   (&optional __integer_value)
   (if __integer_value (setq _integer_value __integer_value)) _integer_value)
  (:float_value
   (&optional __float_value)
   (if __float_value (setq _float_value __float_value)) _float_value)
  (:serialization-length
   ()
   (+
    ;; int8 _integer_value
    1
    ;; float32 _float_value
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int8 _integer_value
       (write-byte _integer_value s)
     ;; float32 _float_value
       (sys::poke _float_value (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int8 _integer_value
     (setq _integer_value (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _integer_value 127) (setq _integer_value (- _integer_value 256)))
   ;; float32 _float_value
     (setq _float_value (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get evaotonom::sign :md5sum-) "86552f94e8d05479ea1a2f8469e502c6")
(setf (get evaotonom::sign :datatype-) "evaotonom/sign")
(setf (get evaotonom::sign :definition-)
      "int8 integer_value
float32 float_value

")



(provide :evaotonom/sign "86552f94e8d05479ea1a2f8469e502c6")


