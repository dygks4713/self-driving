#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
import numpy as np
import math

def degTorad(deg):
    rad_diff = 0.5304
    rad = deg * (3.14/180)
    return rad + rad_diff

def callback(data):
    speed = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)

    range_data = list(data.ranges)[::-1]
    range_data = range_data[319:] + range_data[0:40]

    gs = 0  # widest start gap index
    sum_area = 0
    area_list = []

    threshold = 3  # distance threshold
    n = 3          # minimum gap width

    for i, distance in enumerate(range_data):
        if distance > threshold and not math.isinf(distance):
            if gs == 0:
                gs = i
                sum_area = distance
            else:
                sum_area += distance
        else:
            if gs > 0:  # Closing a gap
                gap_width = i - gs
                if gap_width >= n:
                    area_list.append(
                        {
                            'gs': gs,
                            'ge': i - 1,
                            'gap_width': gap_width,
                            'area': sum_area
                        }
                    )
                gs = 0
                sum_area = 0

    if not area_list:
        gap_width = len(range_data) - gs
        if gap_width > n:
            area_list.append(
                        {
                            'gs': gs,
                            'ge': len(range_data) - 1,
                            'gap_width': gap_width,
                            'area': sum_area
                        }
                    )

    area_list.sort(key=lambda x: (x['gap_width'], x['area']), reverse=True)
    select_gap = area_list[0]
    rospy.loginfo("Selected Gap: {}".format(select_gap))

    gs, ge = select_gap['gs'], select_gap['ge']
    center_index = len(range_data) / 2
    center_gap = (gs + ge) / 2
    position_move = center_gap - center_index
    steering_angle = degTorad(position_move)

    speed.publish(6000)
    position.publish(steering_angle)

    rospy.loginfo("steering : {} ".format(steering_angle))
    rospy.loginfo("center_index: {}".format(center_index))
    rospy.loginfo("position_move: {}".format(position_move))

if __name__ == '__main__':
    try:
        rospy.init_node("tiny_Lidar")
        sub = rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except :
        print("Error occured.")
