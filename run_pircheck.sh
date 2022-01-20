#!/bin/sh

# Ensure backlight mode
sudo sh -c 'echo "0" > /sys/class/backlight/soc\:backlight/brightness'

# Run script
sudo python3 /home/pi/beertap/pir_backlight.py &
exit 0
