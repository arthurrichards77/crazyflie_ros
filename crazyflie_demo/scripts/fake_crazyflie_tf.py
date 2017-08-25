#!/usr/bin/env python  
import roslib
import rospy

import tf
from vicon_bridge.msg import Markers
from math import sqrt

class Tf_faker:

    def __init__(self):
        rospy.init_node('tf_faker')   
        self.br = tf.TransformBroadcaster()

    def marker_callback(self, msg):
        # extract positions
        pos_list = [m.translation for m in msg.markers]
        # assume crazyflie is thing closest to (0,0) ignoring vertical
        dist_list = [sqrt(p.x*p.x + p.y*p.y) for p in pos_list]
        min_dist = min(dist_list)
        cf_pos = [pos_list[ii] for ii in range(len(pos_list)) if dist_list[ii]==min_dist]
        # send fake TF assuming aligned
        self.br.sendTransform((cf_pos[0].x/1000.0,cf_pos[0].y/1000.0,cf_pos[0].z/1000.0),
                     (0, 0, 0, 1),
                     rospy.Time.now(),
                     "crazyflie",
                     "world")

    def start(self):
        rospy.Subscriber('/vicon/markers', Markers,self.marker_callback)


if __name__ == '__main__':
    tfake = Tf_faker()
    tfake.start()
    rospy.spin()
