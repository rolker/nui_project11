#!/usr/bin/env python3

import rospy

from sonardyne_msgs.msg import SMS
from geographic_msgs.msg import GeoPointStamped
from geographic_msgs.msg import GeoPoseStamped
from marine_msgs.msg import Heartbeat
from marine_msgs.msg import KeyValue as HBKeyValue
from std_msgs.msg import Float32

import math
import datetime

import project11
from tf.transformations import quaternion_about_axis

last_state = None

last_positon_time = None

def smsCallback( msg):
  #print(msg)
  if msg.address == '5501':
    hb = Heartbeat()
    hb.header.stamp = msg.receive_time
    kv = HBKeyValue()
    kv.key = 'sms_length'
    kv.value = str(len(msg.message))
    hb.values.append(kv)
    kv = HBKeyValue()
    kv.key = 'receive_time'
    kv.value = datetime.datetime.utcfromtimestamp(msg.receive_time.to_sec()).isoformat()
    hb.values.append(kv)

    heartbeat_pub.publish(hb)

def positionCallback(msg):
  gps = GeoPoseStamped()
  gps.header = msg.header
  gps.pose.position = msg.position
  if last_state is not None:
    if 'timestamp' in last_state and rospy.Time().now() - last_state['timestamp'] < rospy.Duration(secs=300):
      if 'depth' in last_state:
        gps.pose.position.altitude = -last_state['depth']
      if 'heading' in last_state:
        yaw = math.radians(project11.nav.headingToYaw(last_state['heading']))
        quat = quaternion_about_axis(yaw, (0,0,1))
        gps.pose.orientation.x = quat[0]
        gps.pose.orientation.y = quat[1]
        gps.pose.orientation.z = quat[2]
        gps.pose.orientation.w = quat[3]
  position_pub.publish(gps)
  last_positon_time = gps.header.stamp
  #print (msg)

def backupPositionCallback(msg):
  gps = GeoPoseStamped()
  gps.header = msg.header
  gps.pose.position = msg.position
  if last_state is not None:
    if 'timestamp' in last_state and rospy.Time().now() - last_state['timestamp'] < rospy.Duration(secs=300):
      if 'depth' in last_state:
        gps.pose.position.altitude = -last_state['depth']
      if 'heading' in last_state:
        yaw = math.radians(project11.nav.headingToYaw(last_state['heading']))
        quat = quaternion_about_axis(yaw, (0,0,1))
        gps.pose.orientation.x = quat[0]
        gps.pose.orientation.y = quat[1]
        gps.pose.orientation.z = quat[2]
        gps.pose.orientation.w = quat[3]
  if last_positon_time is None or msg.header.stamp - last_positon_time > rospy.Duration(30):
    position_pub.publish(gps)
  #print (msg)


rospy.init_node('nui', anonymous=False)

sms_sub = rospy.Subscriber('sms', SMS, smsCallback)
position_sub = rospy.Subscriber('position', GeoPointStamped, positionCallback)
backup_position_sub = rospy.Subscriber('backup_position', GeoPointStamped, backupPositionCallback)

heartbeat_pub = rospy.Publisher('project11/heartbeat', Heartbeat, queue_size=1)
position_pub = rospy.Publisher('nav/position', GeoPoseStamped, queue_size=1)

rospy.spin()
