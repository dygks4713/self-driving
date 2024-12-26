#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

def degTorad(deg):
    rad_diff= 0.5304
    rad = deg * (3.14/180)
    return rad + rad_diff

def controller():
    speed_pub= rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position_pub= rospy.Publisher('/commands/servo/position', Float64, queue_size=1)
    rospy.init_node('key_controller',anonymous=True)
    speed_pub.publish(10000)
    rospy.sleep(1)
    position_pub.publish(degTorad(10))
    rospy.sleep(1)
    position_pub.publish(degTorad(-10))
    rospy.sleep(1)
    position_pub.publish(degTorad(0))
    rospy.sleep(1)
    speed_pub.publish(0)

if __name__=='__main__':
    controller()
