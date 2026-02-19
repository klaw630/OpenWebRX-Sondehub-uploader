#!/bin/bash
cd /home/pi/upload_v2

/usr/bin/python3 mqtt_to_sondehub.py | /usr/bin/python3 sondehub.py
