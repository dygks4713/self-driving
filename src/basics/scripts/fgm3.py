#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
import math

def degTorad(deg):
    """Convert degrees to radians, including a fixed offset."""
    rad_diff = 0.5304
    rad = deg * (math.pi / 180)
    return rad + rad_diff

def callback(data):
    speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)

    data_range = list(data.ranges)[::-1]
    data_range = data_range[315:] + data_range[0:45]

    gs = 0
    sum_area = 0
    area_list = []

    threshold = 2.7  # Distance threshold for valid gaps
    n = 3          # Minimum gap width

    for i, distance in enumerate(data_range):
        if distance > threshold and not math.isinf(distance):
            if gs == 0:  # Start a new gap
                gs = i
                sum_area = distance
            else:
                sum_area += distance
        else:
            if gs > 0:  # Close the current gap
                gap_width = i - gs
                if gap_width >= n:
                    area_list.append({
                        'gs': gs,
                        'ge': i - 1,
                        'gap_width': gap_width,
                        'area': sum_area
                    })
                gs = 0
                sum_area = 0

    # Handle edge case where last gap reaches the end of the range data
    if gs > 0 and (len(data_range) - gs) >= n:
        area_list.append({
            'gs': gs,
            'ge': len(data_range) - 1,
            'gap_width': len(data_range) - gs,
            'area': sum_area
        })

    if not area_list:
        gap_width = len(data_range) - gs
        area_list.append({
                        'gs': gs,
                        'ge': len(data_range) - 1,
                        'gap_width': gap_width,
                        'area': sum_area
                    })

    # Select the best gap based on width and area
    area_list.sort(key=lambda x: (x['gap_width'], x['area']), reverse=True)
    select_gap = area_list[0]
    rospy.loginfo("Selected Gap: {}".format(select_gap))

    gs, ge = select_gap['gs'], select_gap['ge']
    center_index = len(data_range) / 2
    center_gap = (gs + ge) / 2
    position_move = center_gap - center_index
    steering_angle = degTorad(position_move)

    speed_pub.publish(6000)
    position_pub.publish(steering_angle)

    # Log key variables for debugging
    rospy.loginfo("Steering Angle: {:.2f}, Center Index: {:.2f}, Position Move: {:.2f}".format(
        steering_angle, center_index, position_move
    ))

if __name__ == '__main__':
    try:
        rospy.init_node("tiny_Lidar")
        rospy.Subscriber("/lidar2D", LaserScan, callback)
        rospy.spin()
    except rospy.ROSInterruptException as e:
        rospy.logerr("Error occurred: {}".format(e))
