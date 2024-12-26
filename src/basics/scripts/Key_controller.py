#!/usr/bin/env python
import getch
import rospy
from std_msgs.msg import Float64

gear_state = 'D'  # Initial gear state is Drive

def degTorad(deg):
    # Convert degrees to radians, considering an offset
    rad_diff = 0.5304
    rad = deg * (3.14 / 180)
    return rad + rad_diff

def controller():
    speed = 0.0  # Initial speed
    deg = 0  # Initial steering angle
    position_val = degTorad(0)
    speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)
    position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)
    rospy.init_node('key_controller', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz loop rate

    global gear_state
    while not rospy.is_shutdown():
        k = ord(getch.getch())  

        if k == 113:  # 'q': Exit
            rospy.loginfo("Exit..")
            exit()

        elif k == 119:  # 'w'
            position_val = degTorad(deg)
            if gear_state == 'D':
		if speed <= 10000.0:
	                speed += 1000.0  
		else:
			speed = 15000.0

            elif gear_state == 'R':  
		if speed >= -10000.0:
	                speed -= 1000.0  
		else:
			speed = -15000.0

        elif k == 115:  # 's':
            if speed > 0:
                speed -= 1000.0  
            elif speed < 0:
                speed += 1000.0  

            if abs(speed) < 1000.0:  
                speed = 0.0
            position_val = degTorad(deg)

        elif k == 97:  
            deg -= 1  
            position_val = degTorad(deg)

        elif k == 100:  
            deg += 1  
            position_val = degTorad(deg)

        elif k == 114:  # 'r'
            if gear_state == 'D':
                gear_state = 'R'  
                rospy.loginfo("Gear changed to Reverse")
            else:
                gear_state = 'D'  
                rospy.loginfo("Gear changed to Drive")

        # Publish speed and steering angle
        speed_pub.publish(speed)
        position_pub.publish(position_val)

        # Log current status
        rospy.loginfo("Speed: {}, Steering: {}, Gear: {}".format(speed, position_val, gear_state))
        rate.sleep()

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass

