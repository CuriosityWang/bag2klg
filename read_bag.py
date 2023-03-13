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


parser = argparse.ArgumentParser(description='related')
parser.add_argument('--file_name', '-n', type=str, required=True)
parser.add_argument('--rgb_topic', '-r', type=str,
                    default="/device_0/sensor_1/Color_0/image/data")
parser.add_argument('--depth_topic', '-d', type=str,
                    default="/device_0/sensor_0/Depth_0/image/data")

args = parser.parse_args()


data_dir = "./bag_data"  # path for the bag file
bag_file_name = args.file_name  # bag file name


def mkdirs(path):
    if not os.path.exists(path):
        os.mkdir(path)


def mktxt(path):

    with open(os.path.join(data_dir, path, "rgb.txt"), "a") as f:

        for img in os.listdir(os.path.join(data_dir, path, 'rgb')):
            time_str = img.split(".png")[0]
            file_name = "rgb/" + img
            f.write(time_str + ' ' + file_name + '\n')

    with open(os.path.join(data_dir, path, "depth.txt"), "a") as f:

        for img in os.listdir(os.path.join(data_dir, path, 'depth')):
            time_str = img.split(".png")[0]
            file_name = "depth/" + img
            f.write(time_str + ' ' + file_name + '\n')


if __name__ == "__main__":

    extract_file_path = bag_file_name.split(".bag")[0]
    # absolute path of extracted rgb images
    rgb_path = os.path.join(data_dir, extract_file_path, "rgb")
    # absolute path of extracted depth images
    depth_path = os.path.join(data_dir, extract_file_path, "depth")

    mkdirs(os.path.join(data_dir, extract_file_path))
    mkdirs(rgb_path)
    mkdirs(depth_path)

    bridge = CvBridge()
    print("reading {}".format(args.file_name))
    with rosbag.Bag(os.path.join(data_dir, bag_file_name), 'r') as bag:
        print("extracting rgb and depth images")	 
        for topic,msg,t in bag.read_messages():
            if topic == args.depth_topic: 
                cv_image = bridge.imgmsg_to_cv2(msg, "mono16")
                timestr = "%.8f" %  msg.header.stamp.to_sec()
                image_name = timestr + '.png'# an extension is necessary
                cv2.imwrite(os.path.join(depth_path, image_name), cv_image)
            # print(depth_path + image_name)
            if topic == args.rgb_topic: 
                cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
                timestr = "%.8f" %  msg.header.stamp.to_sec()
                image_name = timestr + '.png'# an extension is necessary
                cv2.imwrite(os.path.join(rgb_path, image_name), cv_image) 

    mktxt(extract_file_path)

    print("Finished")