; Auto-generated. Do not edit!


(cl:in-package evaotonom-msg)


;//! \htmlinclude sign.msg.html

(cl:defclass <sign> (roslisp-msg-protocol:ros-message)
  ((integer_value
    :reader integer_value
    :initarg :integer_value
    :type cl:fixnum
    :initform 0)
   (float_value
    :reader float_value
    :initarg :float_value
    :type cl:float
    :initform 0.0))
)

(cl:defclass sign (<sign>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <sign>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'sign)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name evaotonom-msg:<sign> is deprecated: use evaotonom-msg:sign instead.")))

(cl:ensure-generic-function 'integer_value-val :lambda-list '(m))
(cl:defmethod integer_value-val ((m <sign>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader evaotonom-msg:integer_value-val is deprecated.  Use evaotonom-msg:integer_value instead.")
  (integer_value m))

(cl:ensure-generic-function 'float_value-val :lambda-list '(m))
(cl:defmethod float_value-val ((m <sign>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader evaotonom-msg:float_value-val is deprecated.  Use evaotonom-msg:float_value instead.")
  (float_value m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <sign>) ostream)
  "Serializes a message object of type '<sign>"
  (cl:let* ((signed (cl:slot-value msg 'integer_value)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'float_value))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <sign>) istream)
  "Deserializes a message object of type '<sign>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'integer_value) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'float_value) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<sign>)))
  "Returns string type for a message object of type '<sign>"
  "evaotonom/sign")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'sign)))
  "Returns string type for a message object of type 'sign"
  "evaotonom/sign")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<sign>)))
  "Returns md5sum for a message object of type '<sign>"
  "86552f94e8d05479ea1a2f8469e502c6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'sign)))
  "Returns md5sum for a message object of type 'sign"
  "86552f94e8d05479ea1a2f8469e502c6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<sign>)))
  "Returns full string definition for message of type '<sign>"
  (cl:format cl:nil "int8 integer_value~%float32 float_value~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'sign)))
  "Returns full string definition for message of type 'sign"
  (cl:format cl:nil "int8 integer_value~%float32 float_value~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <sign>))
  (cl:+ 0
     1
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <sign>))
  "Converts a ROS message object to a list"
  (cl:list 'sign
    (cl:cons ':integer_value (integer_value msg))
    (cl:cons ':float_value (float_value msg))
))
