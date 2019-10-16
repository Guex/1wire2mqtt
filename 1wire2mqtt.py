#!/usr/bin/env python
### 1wire to MqTT publisher for all sensors from owfs in json

import time
import os
import paho.mqtt.client as mqtt
import argparse
import ConfigParser
import setproctitle
import json

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
STATUSTOPIC = config.get("mqtt", "statustopic")
POLLINTERVAL = config.getint("mqtt", "pollinterval")
# [OneWire]
OWFS_PATH = config.get("onewire", "owfs_path")
# [log]
LOGFILE = config.get("log", "logfile")
LOGLEVEL = config.getint("log", "loglevel")
# [sensors]
section_name = "sensors"
SENSORS = {}
sensors_files = {}
for name, value in config.items(section_name):
    SENSORS[name] = value.split(',')
APPNAME = "1wire2mqtt"
setproctitle.setproctitle(APPNAME)


## MQTT PUBLISH
def mqtt_connect(TOPIC,sensor_id, json_data):
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT)
    client.publish(topic=TOPIC, payload=json_data, qos=0, retain=False)
    client.disconnect()


def sensor_parse(sensor_id,sensors_files):
    file_name=os.path.join(OWFS_PATH,sensor_id,sensors_files)
    with open(file_name, 'r') as myfile:
        sensor_data = myfile.read()
    return sensor_data

def main_loop():
    while 1:
        for sensor_id in SENSORS:
                     sensor_data={}
                     sensor_type=(SENSORS[sensor_id])
                     for sensors_files in SENSORS[sensor_id]:
                                                    sensor_data[sensors_files]=sensor_parse(sensor_id,sensors_files)
                     ##MAKE TOPIC
                     TOPIC="/"+ STATUSTOPIC+"/" +sensor_id
                     ##MAKE DATA
                     json_data = json.dumps(sensor_data)
                     mqtt_connect(TOPIC,sensor_id,json_data)
        time.sleep(POLLINTERVAL) 

try:
    main_loop()
except KeyboardInterrupt:
    sys.exit(0)
