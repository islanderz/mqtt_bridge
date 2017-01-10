import paho.mqtt.client as mqtt
import datetime

import rospy

def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
#    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    currentTime = datetime.datetime.now();
    timeInMessage = datetime.datetime.strptime(str(msg.payload),"%Y-%m-%d %H:%M:%S.%f");
#   print("Recd at " + str(datetime.datetime.now()));
    print("delay is: " + str((currentTime - timeInMessage).total_seconds() * 1000));

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)


def pingRequestFunction():   
  rospy.init_node('pingRequestFunction');
  mqttc = mqtt.Client()
# Assign event callbacks
  mqttc.on_message = on_message
  mqttc.on_connect = on_connect
  mqttc.on_publish = on_publish
  mqttc.on_subscribe = on_subscribe
  broker = rospy.get_param("~broker","localhost");
  brokerPort = rospy.get_param("~brokerPort",1883);

# Connect
  mqttc.connect(broker, brokerPort,60)
#  mqttc.connect("localhost", 1883,60)

# Start subscribe, with QoS level 0
  mqttc.subscribe("mqtt/pings/response", 0)

# Publish a message
#mqttc.publish("hello/world", "my message")

# Continue the network loop, exit when an error occurs
  rc = 0
  rospy.on_shutdown(mqttc.disconnect);
  rospy.on_shutdown(mqttc.loop_stop)
  lastPublishedTime = datetime.datetime.now();
  while rc == 0:
    rc = mqttc.loop()
    currentTime = datetime.datetime.now();
    if(currentTime - lastPublishedTime > datetime.timedelta(seconds=1)):
      lastPublishedTime = datetime.datetime.now();
      message = str(lastPublishedTime);
      mqttc.publish("mqtt/pings/request",message)
#      print("Sent at " + message);
#time.sleep(1)
  print("rc: " + str(rc))
  print("ping thread disconnected")
