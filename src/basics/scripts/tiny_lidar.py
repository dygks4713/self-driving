#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan

def callback(data):	
    range_data = list(data.ranges)[::-1]
    print('0~30deg dis : ', range_data[0:30])

    #print('0 deg dis : ',data.ranges[0])

    # print('0~30deg dis : ',data.ranges[0:30])

    # print('min of 0~30deg : ',min(data.ranges[0:30]))
	
if __name__ == '__main__':
    try:
        rospy.init_node("ObjectAvoid")
        sub = rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except:
        print("Error occured.")
