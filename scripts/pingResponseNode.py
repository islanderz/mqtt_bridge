#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy

from mqtt_bridge.mqttPingResponder import pingRespondFunction

try:
	pingRespondFunction();
except rospy.ROSInterruptException:
  pass
