from threading import Thread, Lock
from enkoder import enkoder


thread_enkoder=Thread(target=enkoder,args=())
thread_enkoder.start()