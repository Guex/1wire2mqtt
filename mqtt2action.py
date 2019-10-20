#!/usr/bin/env python
### MqTT client for triggering actions

import time
import os
import paho.mqtt.client as mqtt
import argparse
import ConfigParser
import setproctitle
import json
import subprocess

## CONFS
parser = argparse.ArgumentParser( formatter_class=argparse.RawDescriptionHelpFormatter,
description='''reads sensors from 1wire owfs and
publishes to a mqtt-broker''')
parser.add_argument('config_file', metavar="<config_file>", help="file with configuration")
args = parser.parse_args()

# read and parse config file
config = ConfigParser.RawConfigParser()
config.read(args.config_file)
# [mqtt]
MQTT_HOST = config.get("mqtt", "host")
MQTT_PORT = config.getint("mqtt", "port")
PUB_TOPIC = config.get("mqtt", "pub_topic")
PUB_MESSAGE = config.get("mqtt", "pub_message")
# [topic-actions]
section_name = "actions"
topic = {}
topic_actions = {}
for name, value in config.items(section_name):
    topic[name] = value.split(',')
APPNAME = "mqtt2action"
setproctitle.setproctitle(APPNAME)

def exec_command(command):
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        o, e = proc.communicate()
        print('Output: ' + o.decode('ascii'))
        print('Error: '  + e.decode('ascii'))
        print('code: ' + str(proc.returncode))

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    for name in topic:
                    if name == message.topic:
                        print("Publishing message to topic", PUB_TOPIC)
                        client.publish(PUB_TOPIC,PUB_MESSAGE)
                        exec_command(topic[name])
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_start() #start the loop
print("Subscribing to all topics")
client.subscribe("#")
client.loop_forever()

