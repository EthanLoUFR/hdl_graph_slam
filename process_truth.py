#!/usr/bin/env python

"""
Because I am too lazy and too dumb to know how to properly fix things, am just using this script
to bridge topics and whatnot for sake of ease. 

- Republishes ground truth pose with correct frame_id
- Republishes IMU with not completely terrible timestamp
- Should we republish LiDAR? It's not perfect but it's within tolerance I think.
"""

import rospy
import message_filters
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import PointCloud2, Imu

fiducial = None # Initial pose
truth_pub = None
imu_pub = None

def callback(data: PoseStamped):
    now = rospy.Time.now()
    data.header.stamp = now
    data.header.frame_id = "map"

    global fiducial

    if fiducial == None:
        fiducial = data.pose
    
    data.pose.position.x -= fiducial.position.x
    data.pose.position.y -= fiducial.position.y
    data.pose.position.z -= fiducial.position.z
    data.pose.orientation.w -= fiducial.orientation.w
    data.pose.orientation.x -= fiducial.orientation.x
    data.pose.orientation.y -= fiducial.orientation.y
    data.pose.orientation.z -= fiducial.orientation.z

    truth_pub.publish(data)

def bbb(data: Imu):
    now = rospy.Time.now()
    data.header.stamp = now

    imu_pub.publish(data)


if __name__ == "__main__":
    rospy.init_node('process_truth')
    rospy.Subscriber("/truth", PoseStamped, callback)
    rospy.Subscriber("/imu/data", Imu, bbb)

    truth_pub = rospy.Publisher("/sim_truth", PoseStamped, queue_size=10)
    imu_pub = rospy.Publisher("/imu/baddata", Imu, queue_size=10)
    rospy.spin()