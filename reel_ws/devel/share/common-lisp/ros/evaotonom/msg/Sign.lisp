; Auto-generated. Do not edit!


(cl:in-package evaotonom-msg)


;//! \htmlinclude Sign.msg.html

(cl:defclass <Sign> (roslisp-msg-protocol:ros-message)
  ((sign_index
    :reader sign_index
    :initarg :sign_index
    :type cl:fixnum
    :initform 0)
   (depth
    :reader depth
    :initarg :depth
    :type cl:float
    :initform 0.0))
)

(cl:defclass Sign (<Sign>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Sign>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Sign)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name evaotonom-msg:<Sign> is deprecated: use evaotonom-msg:Sign instead.")))

(cl:ensure-generic-function 'sign_index-val :lambda-list '(m))
(cl:defmethod sign_index-val ((m <Sign>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader evaotonom-msg:sign_index-val is deprecated.  Use evaotonom-msg:sign_index instead.")
  (sign_index m))

(cl:ensure-generic-function 'depth-val :lambda-list '(m))
(cl:defmethod depth-val ((m <Sign>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader evaotonom-msg:depth-val is deprecated.  Use evaotonom-msg:depth instead.")
  (depth m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Sign>) ostream)
  "Serializes a message object of type '<Sign>"
  (cl:let* ((signed (cl:slot-value msg 'sign_index)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'depth))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Sign>) istream)
  "Deserializes a message object of type '<Sign>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'sign_index) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'depth) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Sign>)))
  "Returns string type for a message object of type '<Sign>"
  "evaotonom/Sign")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Sign)))
  "Returns string type for a message object of type 'Sign"
  "evaotonom/Sign")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Sign>)))
  "Returns md5sum for a message object of type '<Sign>"
  "9d6f7ebc229c76b7f8002caeee511826")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Sign)))
  "Returns md5sum for a message object of type 'Sign"
  "9d6f7ebc229c76b7f8002caeee511826")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Sign>)))
  "Returns full string definition for message of type '<Sign>"
  (cl:format cl:nil "int8 sign_index~%float32 depth~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Sign)))
  "Returns full string definition for message of type 'Sign"
  (cl:format cl:nil "int8 sign_index~%float32 depth~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Sign>))
  (cl:+ 0
     1
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Sign>))
  "Converts a ROS message object to a list"
  (cl:list 'Sign
    (cl:cons ':sign_index (sign_index msg))
    (cl:cons ':depth (depth msg))
))
