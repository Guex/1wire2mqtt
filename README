This is 1wire (onewire) owfs gateway to MQTT broker written in python.
It takes information from files on mounted fuse.OWFS filesystem
and sending all collected information to MQTT in json.
Tested on rapsbian pi 10.1, but it must works well on other systems with python 2.7

Requirements:
apt-get install python python-paho-mqtt python-ConfigParser python-setproctitle
installed and mounted owfs, for example:

root@raspberrypi:~/1wire2mqtt# ls -la /mnt/1wire/
total 4
drwxr-xr-x 1 root root 4096 Oct 13 14:59 .
drwxr-xr-x 3 root root 4096 Oct 12 11:00 ..
drwxrwxrwx 1 root root 4096 Oct 16 15:13 1D.6A9306000000
drwxrwxrwx 1 root root 4096 Oct 16 15:13 26.DA2F71010000
drwxrwxrwx 1 root root 4096 Oct 16 15:13 28.0425260A0000
drwxrwxrwx 1 root root 4096 Oct 16 15:13 28.48B3010B0000
drwxrwxrwx 1 root root 4096 Oct 16 15:13 28.61CC260A0000
drwxrwxrwx 1 root root 4096 Oct 16 15:13 28.BF16270A0000
drwxr-xr-x 1 root root 4096 Oct 13 14:59 alarm
drwxr-xr-x 1 root root 4096 Oct 13 14:59 bus.1
drwxr-xr-x 1 root root 4096 Oct 13 14:59 settings
drwxrwxrwx 1 root root 4096 Oct 16 15:13 simultaneous
drwxr-xr-x 1 root root 4096 Oct 13 14:59 statistics
drwxr-xr-x 1 root root 4096 Oct 13 14:59 structure
drwxr-xr-x 1 root root 4096 Oct 13 14:59 system
drwxr-xr-x 1 root root 4096 Oct 13 14:59 uncached


Configuration
read 1wire2mqtt.cfg comments
You can add all needed file names to parse in case "filename" : "value" from owfs_path.
For example /mnt/1wire/28.BF16270A0000/
total 0
drwxrwxrwx 1 root root 4096 Oct 16 15:18 .
drwxr-xr-x 1 root root 4096 Oct 13 14:59 ..
-r--r--r-- 1 root root   16 Oct 13 14:59 address
-rw-rw-rw- 1 root root  256 Oct 13 14:59 alias
-r--r--r-- 1 root root    2 Oct 13 14:59 crc8
drwxrwxrwx 1 root root 4096 Oct 16 15:18 errata
-r--r--r-- 1 root root    2 Oct 13 14:59 family
-r--r--r-- 1 root root   12 Oct 13 14:59 fasttemp
-r--r--r-- 1 root root   12 Oct 13 14:59 id
-r--r--r-- 1 root root   12 Oct 16 15:18 latesttemp
-r--r--r-- 1 root root   16 Oct 13 14:59 locator
-r--r--r-- 1 root root    1 Oct 16 15:18 power
-r--r--r-- 1 root root   16 Oct 13 14:59 r_address
-r--r--r-- 1 root root   12 Oct 13 14:59 r_id
-r--r--r-- 1 root root   16 Oct 13 14:59 r_locator
-r--r--r-- 1 root root    9 Oct 16 15:18 scratchpad
-r--r--r-- 1 root root   12 Oct 13 14:59 temperature
-r--r--r-- 1 root root   12 Oct 13 14:59 temperature10
-r--r--r-- 1 root root   12 Oct 13 14:59 temperature11
-r--r--r-- 1 root root   12 Oct 13 14:59 temperature12
-r--r--r-- 1 root root   12 Oct 13 14:59 temperature9
-rw-rw-rw- 1 root root   12 Oct 16 15:18 temphigh
-rw-rw-rw- 1 root root   12 Oct 16 15:18 templow
-rw-rw-rw- 1 root root   12 Oct 16 15:18 tempres
-r--r--r-- 1 root root   32 Oct 13 14:59 type

So, you can add 28.BF16270A0000 = type,temperature
And it will open type and temperature file for sending
/1wire/28.bf16270a0000 {"type": "DS18B20", "temperature": "8.125"}

Or even you can use this gateway for sending not only owfs data to MQTT.

To run at boot, make the script exutable:
chmod +x /your_folder/1wire2mqtt.py
and add this to your rc.local:
/your_folder/1wire2mqtt.py 1wire2mqtt.cfg &

