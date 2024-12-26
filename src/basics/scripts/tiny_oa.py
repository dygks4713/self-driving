#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan

def degTorad(deg):
	rad_diff = 0.5304
	rad = deg * (3.14/180)
	return rad + rad_diff

def callback(data):	
    speed = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)

    range_data= list(data.ranges)[::-1]

    if min(range_data[0:30]) < 3 or min(range_data[330:359]) < 3:
	if min(range_data[0:30]) < min(range_data[330:359]):
		position.publish(degTorad(-10))
	else:
		position.publish(degTorad(10))
    else:
	position.publish(degTorad(0))

    speed.publish(7000)

if __name__ == '__main__':
    try:
        rospy.init_node("Tiny_ObjectAvoid")
        sub = rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except:
        print("Error occured.")
