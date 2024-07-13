cmake_minimum_required(VERSION 3.0.2)
project(evaotonom) 

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  sensor_msgs
)

catkin_package(
  INCLUDE_DIRS include  # Header dosyalarının bulunduğu klasör 
  LIBRARIES evaotonom  # Oluşturulacak kütüphane adı
  CATKIN_DEPENDS roscpp rospy std_msgs sensor_msgs  # Bağımlılıklar
)

include_directories(include ${catkin_INCLUDE_DIRS})

catkin_install_python(PROGRAMS scripts/reel-obstacle-detect.py scripts/reel-lane-track.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
