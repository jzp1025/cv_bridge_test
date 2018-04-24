# !/usr/bin/python
"""
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
Updated: Copyright (c) 2016, Tal Regev.
"""

import sys
import os
from optparse import OptionParser

import rclpy
import sensor_msgs.msg
from cv_bridge import CvBridge
import cv2
import numpy


def detect_and_draw(imgmsg):
   
    print(type(imgmsg.data))

    br = CvBridge()
    img = br.imgmsg_to_cv2(imgmsg)
    # allocate temporary images
    
    # convert color input image to grayscale
    print("success")   
 
    cv2.imshow("result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

def compressed_detect_and_draw(compressed_imgmsg):
    img = br.compressed_imgmsg_to_cv2(compressed_imgmsg, "bgr8")
    # allocate temporary images
    new_size = (int(img.shape[1] / image_scale), int(img.shape[0] / image_scale))

    # convert color input image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # scale input image for faster processing
    small_img = cv2.resize(gray, new_size, interpolation = cv2.INTER_LINEAR)

    small_img = cv2.equalizeHist(small_img)

    if(cascade):
        faces = cascade.detectMultiScale(small_img, haar_scale, min_neighbors, haar_flags, min_size)
        if faces is not None:
            for (x, y, w, h) in faces:
                # the input to detectMultiScale was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                cv2.rectangle(img, pt1, pt2, (255, 0, 0), 3, 8, 0)

    cv2.imshow("compressed_result", img)
    cv2.waitKey(6)

def main(args=None):
    if args is None:
        args = sys.argv
    rclpy.init(args=args)

    # TODO add this file in the repository and make it relative to this python script. (not all people will run this from linux)
  
    br = CvBridge()

    node = rclpy.create_node('rosfacedetect')
    node_logger = node.get_logger()
    sub_img = node.create_subscription(sensor_msgs.msg.Image, "/opencv_tests/images", detect_and_draw)
    #sub_cpimg = node.create_subscription(sensor_msgs.msg.CompressedImage, "/opencv_tests/images/compressed", compressed_detect_and_draw)

    while rclpy.ok():
      try:
        rclpy.spin_once(node)
      except KeyboardInterrupt:
        node_logger.info("shutting down: keyboard interrupt")
        break

    node_logger.info("test_completed")
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
