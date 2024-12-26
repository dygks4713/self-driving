#!/usr/bin/env python
import getch
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan

def callback(data):	
    speed = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)

    range_data= list(data.ranges)[::-1]

    if min(range_data[0:30]) < 2 or min(range_data[330:359]) < 2:
        speed.publish(0)
    else:
        speed.publish(7000)

if __name__ == '__main__':
    try:
        rospy.init_node("StopandGo")
        sub = rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except:
        print("Error occured.")
