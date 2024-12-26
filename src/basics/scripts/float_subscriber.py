#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float32
def callback(msg):
	print("{:.1f}".format(msg.data))

rospy.init_node('float_publisher.py')
sub = rospy.Subscriber('counter', Float32, callback)
rospy.spin()

