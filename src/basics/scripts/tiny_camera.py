#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from std_msgs.msg import Float64
from sensor_msgs.msg import CompressedImage

def callback(image):
    np_arr= np.fromstring(image.data, np.uint8) 
    cv_image= cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    cv2.imshow('camera_test', cv_image), cv2.waitKey(1) 
	
if __name__ == '__main__':
    try:
        rospy.init_node("CameraTest")
        sub = rospy.Subscriber("/image_jpeg/compressed", CompressedImage, callback)
        rospy.spin()
    except:
        print("Error occured.")
