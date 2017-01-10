import paho.mqtt.client as mqtt
import datetime

import rospy

def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
#    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    mosq.publish("mqtt/pings/response",str(msg.payload));
#   currentTime = datetime.datetime.now();
#   timeInMessage = datetime.datetime.strptime(str(msg.payload),"%Y-%m-%d %H:%M:%S.%f");
#   print("Recd at " + str(datetime.datetime.now()));
#   print("delay is: " + str((currentTime - timeInMessage).total_seconds() * 1000));

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)


def pingRespondFunction():   

  rospy.init_node('pingRespondFunction');

  broker = rospy.get_param("~broker","localhost");
  brokerPort = rospy.get_param("~brokerPort",1883);
  mqttc = mqtt.Client()
# Assign event callbacks
  mqttc.on_message = on_message
  mqttc.on_connect = on_connect
  mqttc.on_publish = on_publish
  mqttc.on_subscribe = on_subscribe
# Connect
  mqttc.connect(broker, brokerPort,60)
#  mqttc.connect("localhost", 1883,60)

# Start subscribe, with QoS level 0
  mqttc.subscribe("mqtt/pings/request", 0)

# Publish a message
#mqttc.publish("hello/world", "my message")

# Continue the network loop, exit when an error occurs
  rc = 0
  lastPublishedTime = datetime.datetime.now();
  rospy.on_shutdown(mqttc.disconnect);
  rospy.on_shutdown(mqttc.loop_stop);
  while rc == 0:
    rc = mqttc.loop()
#    currentTime = datetime.datetime.now();
#    if(currentTime - lastPublishedTime > datetime.timedelta(seconds=1)):
#      lastPublishedTime = datetime.datetime.now();
#      message = str(lastPublishedTime);
#      mqttc.publish("f",message)
#      print("Sent at " + message);
#time.sleep(1)
  print("rc: " + str(rc))
  print("ping thread disconnected")
