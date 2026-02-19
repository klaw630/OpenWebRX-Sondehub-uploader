# OpenWebRX-Sondehub-uploader
Uploads received sonde data to https://sondehub.org/  
THIS IS HIGHLY UNDER DEVELOPMENT!!!!!  
The program gets sonde data via MQTT, so if you want to change the MQTT address, its in the `mqtt_to_sondehub.py`.  
The `run_uploader.sh` should be run from crontab (or atleast that's what I did), so you will upload at the right times.
If your directory is not `/home/pi/upload_v2/` like mine, also change that!  
