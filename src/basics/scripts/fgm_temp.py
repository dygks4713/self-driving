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
    
    range_data = list(data.ranges)[::-1]	
    range_data = range_data[330:359] + range_data[0:30]

    i = 0
    gs = 0 #widest start gap index
    ge = 0 #widest end gap index
    ts = 0
    
    #set threshold t
    threshold = 3
    #set gap n
    n = 3

    #calculate gap width and select widest gap
    for data in range_data:
        if data > threshold and gs == ts:
            ts = i
        elif data <= threshold and gs != ts:
	    if (ge-gs) < (i - ts) and (i - ts) >= n:
                gs = ts
                ge = i
        i += 1

    if gs != ts:
        gs = ts
	ge = i-1

    range_print = [ '%.2f' % elem for elem in range_data ]
    print(range_print)

if __name__ == '__main__':
    try:
        rospy.init_node("tiny_Lidar")
        sub = rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except:
        print("Error occured.")
