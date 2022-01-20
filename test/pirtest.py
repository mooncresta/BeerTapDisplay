import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN)         #Read output from PIR motion sensor

#f = open("/sys/class/graphics/fb1/blank")
prev = 99
#f.write('1')

while True:
   i=GPIO.input(37)
   if i == prev:
      # Same state
      prev = i
   else:
      if i==0:                 #When output from motion sensor is LOW
          print("No intruders {0}".format(i))
#          f.write("0
          time.sleep(0.5)
      elif i==1:               #When output from motion sensor is HIGH
          print("Intruder detected {0}".format(i))
          time.sleep(0.5)
      prev = i
