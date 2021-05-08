import OPi.GPIO as GPIO
import time
import os, sys

HOST = '127.0.0.1'
PORT = 8085
fpid = os.fork()
if fpid!=0:
 sys.exit(0)


GPIO.setmode(GPIO.SUNXI)
GPIO.setwarnings(False)
GPIO.setup('PA12', GPIO.OUT)  # green LED
GPIO.setup('PA11', GPIO.OUT)  # red LED

# when we initialise, the LEDs go out, this is the expected behaviour


# this loop handles the LED flash modes
while True:
 GPIO.output('PA12', GPIO.HIGH)
 time.sleep(0.1)
 GPIO.output('PA12', GPIO.LOW)
 time.sleep(1)
