import paho.mqtt.client as paho
import sys

client = paho.Client()

if client.connect("localhost", 1883, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)

test = [1,2,3,4]
listTostr = ' '.join(str(elem) for elem in test)
client.publish("test/status", listTostr, 0)

client.disconnect()