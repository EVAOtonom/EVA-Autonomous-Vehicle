import rospy
from sensor_msgs.msg import LaserScan


def lidar_callback(msg):
    
    ranges = msg.ranges
    intensities = msg.intensities
    print("Lidar Ranges:", ranges)
    print("Lidar Intensities:", intensities)

def main():
    rospy.init_node('lidar_subscriber') 

    
    rospy.Subscriber("/lidar/laser/scan", LaserScan, lidar_callback)

    
    rospy.spin()

if __name__ == '__main__':
    main()