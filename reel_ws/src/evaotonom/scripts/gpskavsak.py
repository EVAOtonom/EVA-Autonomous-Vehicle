import rospy
from std_msgs.msg import Float32, Int8

# Dikdörtgen alanı belirleyen koordinatlar
rect_area = [
    (41.057495, 28.820268),
    (41.057487, 28.820335),
    (41.057452, 28.820263),
    (41.057432, 28.820311)
]

# Yardımcı fonksiyon: Bir noktanın belirli bir alan içinde olup olmadığını kontrol eder
def is_within_area(lat, lon, area):
    min_lat = min(point[0] for point in area)
    max_lat = max(point[0] for point in area)
    min_lon = min(point[1] for point in area)
    max_lon = max(point[1] for point in area)
    return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon

# Global değişkenler
latitude = None
longitude = None

# Sapma düzeltme faktörleri
lat_correction = -0.0001
lon_correction = -0.000032

def latitude_callback(msg):
    global latitude
    latitude = msg.data

def longitude_callback(msg):
    global longitude
    longitude = msg.data

if __name__ == "__main__":
    rospy.init_node('gps_checker', anonymous=True)

    # Subscribers
    rospy.Subscriber('gps_latitude', Float32, latitude_callback)
    rospy.Subscriber('gps_longitude', Float32, longitude_callback)

    # Publishers
    kavsak_noktasi_pub = rospy.Publisher("/sign_detector/roundabout", Int8, queue_size=10)

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        if latitude is not None and longitude is not None:
            corrected_latitude = latitude + lat_correction
            corrected_longitude = longitude + lon_correction
            print(corrected_latitude, corrected_longitude)
            if is_within_area(corrected_latitude, corrected_longitude, rect_area):
                kavsak_noktasi_pub.publish(1)
                rospy.loginfo("Kavşak")
            else:
                kavsak_noktasi_pub.publish(0)  # Kavşak değilse 0 yayınla
        rate.sleep()
