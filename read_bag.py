import roslib
import rosbag
import rospy
import cv2
import numpy as np
import os
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from cv_bridge import CvBridgeError
import argparse



data_dir = "./bag_data" # set path for the bag file
bag_file_name = "600.bag" # bag file name


def mkdirs(path):
    if not os.path.exists(path):
        os.mkdir(path)

    

def mktxt(path):

    with open(os.path.join(data_dir, path, "rgb.txt"), "a") as f:

        for img in os.listdir(os.path.join(data_dir, path, 'rgb')):
            time_str = img.split(".png")[0]
            file_name = "rgb/" +  img
            f.write(time_str + ' ' + file_name + '\n')

    with open(os.path.join(data_dir, path, "depth.txt"), "a") as f:

        for img in os.listdir(os.path.join(data_dir, path, 'depth')):
            time_str = img.split(".png")[0]
            file_name = "depth/" +  img
            f.write(time_str + ' ' + file_name+ '\n')



if __name__=="__main__":

    extract_file_path = bag_file_name.split(".bag")[0]
    # rgb_path = os.path.join(data_dir, extract_file_path, "rgb") # absolute path of extracted rgb images
    # depth_path = os.path.join(data_dir, extract_file_path, "depth") # absolute path of extracted depth images

    # mkdirs(os.path.join(data_dir, extract_file_path))
    # mkdirs(rgb_path)
    # mkdirs(depth_path)


    # bridge = CvBridge()
    # with rosbag.Bag(os.path.join(data_dir, bag_file_name), 'r') as bag:
    #     for topic,msg,t in bag.read_messages():
    #         if topic == "/device_0/sensor_0/Depth_0/image/data": 
    #             cv_image = bridge.imgmsg_to_cv2(msg, "mono16")
    #             timestr = "%.8f" %  msg.header.stamp.to_sec()
    #             image_name = timestr + '.png'# an extension is necessary
    #             cv2.imwrite(os.path.join(depth_path, image_name), cv_image)
    #         # print(depth_path + image_name)
    #         if topic == "/device_0/sensor_1/Color_0/image/data": 
    #             cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    #             timestr = "%.8f" %  msg.header.stamp.to_sec()
    #             image_name = timestr + '.png'# an extension is necessary
    #             cv2.imwrite(os.path.join(rgb_path, image_name), cv_image) 


    mktxt(extract_file_path)