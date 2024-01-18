#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from rplidar import RPLidar

def lidar_publisher():
    rospy.init_node('lidar_publisher', anonymous=True)

    port_name = rospy.get_param("~port_name", "/dev/ttyUSB0")
    lidar = RPLidar(
        port_name, baudrate=256000, timeout=2)
    lidar_pub = rospy.Publisher('lidar_scan', LaserScan, queue_size=10)

    try:
        rospy.loginfo("Lidar node is running...")
        rospy.sleep(0.5)

        for bool, lazer_gucu, angle, distance in lidar.iter_measurments(max_buf_meas=500):
            if 360 > angle > 350 or 10 > angle > 0:
                lidar_data = LaserScan()
                lidar_data.header.stamp = rospy.Time.now()
                lidar_data.header.frame_id = "lidar_frame"
                lidar_data.angle_min = 0.0
                lidar_data.angle_max = 2.0 * 3.14159
                lidar_data.angle_increment = 0.0175
                lidar_data.time_increment = 0.0
                lidar_data.scan_time = 0.1
                lidar_data.range_min = 0.1
                lidar_data.range_max = 10.0
                lidar_data.ranges = [distance]

                lidar_pub.publish(lidar_data)

    except rospy.ROSInterruptException:
        rospy.loginfo("Lidar node stopped by user.")
    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == '__main__':
    lidar_publisher()