#!/usr/bin/env python3

import rospy
import socket

from std_msgs.msg import String

rospy.init_node("udp_to_sms")

port = rospy.get_param("~port", 2884)
buffer_size = rospy.get_param("~buffer_size", 2048)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', port))
s.settimeout(0.1)

str_pub = rospy.Publisher("output", String, queue_size=1)

while not rospy.is_shutdown():
  try:
    data = s.recv(buffer_size)
    msg = String()
    msg.data = data
    str_pub.publish(msg)
  except socket.timeout:
    pass
