# Home Assistant by J-Lindvig
![Main screen](https://github.com/J-Lindvig/Home-Assistant-Master/raw/master/www/images/screenshots/scr_main_1.png)
This is my implementation of Home Assistant, it may not be for the faint of heart - but it is mine and I like it....
Please enjoy my madness and use what you can.
## Introduction
In my setup I rely heavily on YAML and plugins like [lovelace_gen](https://github.com/thomasloven/hass-lovelace_gen) and [layout-card](https://github.com/thomasloven/lovelace-layout-card).
I absolutely hate "hard-coding" and will go a great length to make my cards, scripts and automations as flexible as possible. 
# Hardware
 - Raspberry Pi 3B+
   - PNY 240 GB SSD USB3.1
 - Xiaomi Roborock S50 vacuum
 - Conbee II with 135 units
 - IKEA TRÅDFRI
 - 2 Tuya Smartswitches
 - 3 Broadlink 3 rm mini
 - 3 Sonoff RF bridges with Tasmota and Portisch
### Software
I have the following add-ons installed:
- MariaDB
- deCONZ
- MQTT Broker
- Google Drive Backup
- File editor
- SSH & Web Terminal
- Samba share
- RPC Shutdown
- Check Home Assistant configuration
- phpMyAdmin
## Configuration
My setup is heavily divided with `!include` and *packages* in multiple directories.
### Files
[configuration.yaml](https://github.com/J-Lindvig/HomeAssistant/blob/master/configuration.yaml)
> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbODI0MDAwNTY0XX0=
-->