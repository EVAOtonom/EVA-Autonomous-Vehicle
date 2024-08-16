
(cl:in-package :asdf)

(defsystem "evaotonom-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Sign" :depends-on ("_package_Sign"))
    (:file "_package_Sign" :depends-on ("_package"))
  ))