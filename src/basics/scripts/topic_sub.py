#! /usr/bin/env python

import rospy
from std_msgs.msg import Int32

PI = 3.14

def callback(msg):
    circle_area = ((msg.data/2) ** 2) * PI
    print("Area of circle : {:.2f}".format(circle_area))

rospy.init_node('topic_subscriber')
sub = rospy.Subscriber('counter', Int32, callback)

rospy.spin()
