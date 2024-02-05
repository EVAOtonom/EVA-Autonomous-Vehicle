#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from rplidar import RPLidar

def lidar_publisher():
    rospy.init_node('lidar_publisher', anonymous=True)

    port_name = rospy.get_param("~port_name", "/dev/ttyUSB1")
    lidar = RPLidar(port_name, baudrate=256000, timeout=3)
    lidar_pub = rospy.Publisher('lidar_scan', LaserScan, queue_size=10)

    try:
        rospy.loginfo("Lidar node is running...")
        #rospy.sleep(0.5)

        for scan in lidar.iter_scans():
            lidar_data = LaserScan()
            lidar_data.header.stamp = rospy.Time.now()
            lidar_data.header.frame_id = "lidar_frame"
            lidar_data.angle_min = -3.14159
            lidar_data.angle_max = 2.0 * 3.14159 
            lidar_data.angle_increment = 0.0175
            lidar_data.time_increment = 0.0
            lidar_data.scan_time = 0.1
            lidar_data.range_min = 0.1
            lidar_data.range_max = 10.0
            # Tüm açılar için bir mesafe dizisi oluştur
            num_readings = int(round((lidar_data.angle_max - lidar_data.angle_min) / lidar_data.angle_increment))
            lidar_data.ranges = [float('Inf')] * num_readings

            for (_, angle, distance) in scan:
                if angle <= 10 or angle >= 350:
                    # Açıyı radiana çevir ve indeksi hesapla
                    angle_radians = angle * (3.14159 / 180.0)
                    index = int((angle_radians - lidar_data.angle_min) / lidar_data.angle_increment)
                    if 0 <= index < num_readings:  # İndeks sınırları kontrol et
                        lidar_data.ranges[index] = distance 
                    lidar_pub.publish(lidar_data)


    except rospy.ROSInterruptException:
        rospy.loginfo("Lidar node stopped by user.")
    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == '__main__':
    lidar_publisher() 
           
    