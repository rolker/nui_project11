#!/usr/bin/env python3

import rospy
import socket

from std_msgs.msg import String

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 5000))
s.settimeout(0.1)

rospy.init_node("udp_to_sms")

usbl_pub = rospy.Publisher("/project11/drix_8/usbl_modem/send_raw", String, queue_size=1)

while not rospy.is_shutdown():
  try:
    data = s.recv(2048)
    print (data)
    if len(data) and data[0] == '<':
      usbl_msg = String()
      usbl_msg.data = data
      usbl_pub.publish(usbl_msg)
  except socket.timeout:
    pass
