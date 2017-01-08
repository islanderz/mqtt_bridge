#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy

from mqtt_bridge.mqttPingRequester import pingRequestFunction

try:
	pingRequestFunction();
except rospy.ROSInterruptException:
  pass
