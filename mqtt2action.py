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
import csv
import re
import threading

## CONFS
parser = argparse.ArgumentParser( formatter_class=argparse.RawDescriptionHelpFormatter,
description='''reads sensors from 1wire owfs and
publishes to a mqtt-broker''')
parser.add_argument('config_file', metavar="<config_file>", help="file with configuration")
args = parser.parse_args()

# read and parse config file
config = ConfigParser.RawConfigParser()
config.read(args.config_file)
KEYFILE = config.get("global", "keyfile")
# [mqtt]
MQTT_HOST = config.get("mqtt", "host")
MQTT_PORT = config.getint("mqtt", "port")
PUB_TOPIC = config.get("mqtt", "pub_topic")
PUB_MESSAGE = config.get("mqtt", "pub_message")
APPNAME = "mqtt2action"
setproctitle.setproctitle(APPNAME)

global timelastrun
timelastrun = 0

class KeyMap:
    """
    Read the topics and keys into a dictionary for internal lookups
    """
    with open(KEYFILE, mode="r") as inputfile:
        reader = csv.reader(inputfile,delimiter=':')
        mapdict = dict((rows[0], rows[1]) for rows in reader)

def exec_command(command):
        print("Exec_command executing")
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        o, e = proc.communicate()
        print('Output: ' + o.decode('ascii'))
        print('Error: '  + e.decode('ascii'))
        print('code: ' + str(proc.returncode))
        global timelastrun
        timelastrun = int(time.time())
#def exec_command(command):
#    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#    o, e = proc.communicate()
#    print('Output: ' + o.decode('ascii'))
#    print('Error: '  + e.decode('ascii'))
#    print('code: ' + str(proc.returncode))
#    sleep(5)


def listToString(s):  
    # initialize an empty string 
    str1 = ""  
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    # return string   
    return str1  

def on_message(client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)
        for itemKey in KeyMap.mapdict:
            (itemTopic,itemData)=itemKey.split(",")
            if itemTopic == message.topic:
                if itemData in listToString(message.payload.decode("utf-8")):
                    print("itemTopic:", itemTopic)
                    print("Publishing message to topic", PUB_TOPIC, itemData)
                    client.publish(PUB_TOPIC,PUB_MESSAGE)
                    itemAction=KeyMap.mapdict[itemKey]
                    print("TimeLastRun:", timelastrun)
                    if int(time.time()) - timelastrun < 5:
                        print("Time lock, skip command executing", timelastrun)
                    else:
                        print("itemAction:", itemAction, "Runtime:", timelastrun)
                        exec_command(itemAction)

client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(MQTT_HOST, MQTT_PORT)
#client.loop_start() #start the loop
print("Subscribing to all topics")
client.subscribe("#")
client.loop_forever()
