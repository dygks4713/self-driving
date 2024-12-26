#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float32

rospy.init_node('topic_publisher')
pub = rospy.Publisher('counter', Float32, queue_size=10)
rate = rospy.Rate(1)
count = 0.1

while not rospy.is_shutdown():
	pub.publish(count)
	count += 0.1
	rate.sleep()

