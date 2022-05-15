#!/usr/bin/env python3

import rospy
import socket

from std_msgs.msg import String

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def onString(msg):
  s.sendto(msg.data.encode('utf-8'), ('192.168.8.235',5000))

rospy.init_node("string_to_udp")

rospy.Subscriber("/project11/drix_8/usbl/telegrams", String, onString)

rospy.spin()
