This is 1wire (onewire) owfs gateway to MQTT broker written in python.
It takes information from files on mounted fuse.OWFS filesystem
and sending all collected information to MQTT in json.
Tested on rapsbian pi 10.1, but it must works well on other systems with python 2.7

Requirements:
apt-get install python python-paho-mqtt python-ConfigParser python-setproctitle
installed and mounted owfs, for example:

root@raspberrypi:~/1wire2mqtt# ls /mnt/1wire/

1D.6A9306000000  26.DA2F71010000  28.0425260A0000  28.48B3010B0000  28.61CC260A0000  28.BF16270A0000  alarm  bus.1  settings  simultaneous  statistics	structure  system  uncached


Configuration

read 1wire2mqtt.cfg comments
You can add all needed file names to parse in case "filename" : "value" from owfs_path.

For example:

root@raspberrypi:~/1wire2mqtt# ls /mnt/1wire/28.BF16270A0000/

address  crc8	 family    id	       locator	r_address  r_locator   temperature    temperature11  temperature9  templow  type
alias	 errata  fasttemp  latesttemp  power	r_id	   scratchpad  temperature10  temperature12  temphigh	   tempres


So, you can add 28.BF16270A0000 = type,temperature
And it will open type and temperature file for sending
/1wire/28.bf16270a0000 {"type": "DS18B20", "temperature": "8.125"}

Or even you can use this gateway for sending not only owfs data to MQTT.

To run at boot, make the script executable:
chmod +x /your_folder/1wire2mqtt.py
and add this to your rc.local:
/your_folder/1wire2mqtt.py /your_folder/1wire2mqtt.cfg &

