# 1wire2mqtt/mqtt2action for Python3
This is a 1wire (onewire) owfs gateway to MQTT broker written in python.
It got forked from (<https://github.com/unlo/1wire2mqtt>) and adapted to work python 3.
It takes information from files on mounted fuse.OWFS filesystem
and sending all collected information to MQTT in json.
1wire2mqtt tested on rapsbian pi 13, but it should work on other systems as well.
mqtt2action is not tested at all.

## Requirements
apt-get install python3-minimal python3-paho-mqtt python3-setproctitle
installed and mounted owfs, for example:

root@raspberrypi:~/1wire2mqtt# ls /run/owfs/

1D.6A9306000000  26.DA2F71010000  28.0425260A0000  28.48B3010B0000  28.61CC260A0000  28.BF16270A0000  alarm  bus.1  settings  simultaneous  statistics	structure  system  uncached

## Configuration

read 1wire2mqtt.cfg comments
You can add all needed file names to parse in case "filename" : "value" from owfs_path.

For example:

root@raspberrypi:~/1wire2mqtt# ls /run/owfs/28.BF16270A0000/

address  crc8	 family    id	       locator	r_address  r_locator   temperature    temperature11  temperature9  templow  type
alias	 errata  fasttemp  latesttemp  power	r_id	   scratchpad  temperature10  temperature12  temphigh	   tempres

So, you can add 28.BF16270A0000 = type,temperature
And it will open type and temperature file for sending
/1wire/28.bf16270a0000 {"type": "DS18B20", "temperature": "8.125"}

Or even you can use this gateway for sending not only owfs data to MQTT.

## Autostart

Use either of the following variants (systemd prefferred) to autostart the service.

### Systemd

Adjust below example and save it (as root) to "/etc/systemd/system/1wire2mqtt.service".
~~~
[Unit]
Description=1wire2mqtt service
#define any required service, like a wireguard vpn here
#Requires=wg-quick@wg0.service
#After=wg-quick@wg0.service
StartLimitIntervalSec=0

[Service]
User=your_user
WorkingDirectory=/tmp
ExecStart=/usr/bin/python3 /your_folder/1wire2mqtt/1wire2mqtt.py  /your_folder/1wire2mqtt/1wire2mqtt.cfg
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
~~~

Then enable and start the service accordingly.
~~~
systemctl enable 1wire2mqtt
systemctl start 1wire2mqtt
~~~

### rc script
To run at boot, make the script executable:

and add this to your rc.local:
~~~
/usr/bin/python3 /your_folder/1wire2mqtt.py /your_folder/1wire2mqtt.cfg &
~~~