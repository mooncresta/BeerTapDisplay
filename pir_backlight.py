#import RPi.GPIO as GPIO
import time
import board
#import pwmio
import digitalio


# For Adafruit PITFT

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(37, GPIO.IN)         #Read output from PIR motion sensor

prev = 99
pir = digitalio.DigitalInOut(board.D26)
pir.direction = digitalio.Direction.INPUT
backlight = digitalio.DigitalInOut(board.D18)
backlight.direction = digitalio.Direction.OUTPUT
# Turn on backlight initially
backlight.value = True
time.sleep(60)

while True:
   # Read PIR
#   i=GPIO.input(37)
   i = pir.value

   if i == prev:
      # Same state
      prev = i
      time.sleep(1)
   else:
      if i==0:                 #When output from motion sensor is LOW
#          print("No intruders {0}".format(i))
          # Turn Backlight off
          backlight.value = False
      elif i==1:               #When output from motion sensor is HIGH
#          print("Intruder detected {0}".format(i))
          backlight.value = True
          time.sleep(60)
      prev = i
