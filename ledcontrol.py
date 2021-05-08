import socket
import threading
import time
import OPi.GPIO as GPIO
import os, sys

ledflashrate = 0
redledmode = 0   # 0 = off, 1 = on, 2 = flash 50% duty cycle, 3 = flash 10% duty cycle

red_memory = 0
green_memory = 0



fpid = os.fork()
if fpid!=0:
   sys.exit(0)

def setGreenLed(state):
  global green_memory
  if state != green_memory:
    green_memory = state
    # there was a change so we can write to gpio
    if state == 0:
     GPIO.output('PA12', GPIO.LOW)

    if state == 1:
     GPIO.output('PA12', GPIO.HIGH)

def setRedLed(state):
  global red_memory
  if state != red_memory:
    red_memory = state
    # there was a change so we can write to gpio
    if state == 0:
     GPIO.output('PA11', GPIO.LOW)
    if state == 1:
     GPIO.output('PA11', GPIO.HIGH)




# Thread code, runs at 1mS intervals
def led_control_thread():
   redledtoggle = 0
   redledcycle = 500
   greenledcycle = 500
   greenledtoggle = 0
   redshortcycle = 100
   greenshortcycle = 100
   redlongcycle = 900
   greenlongcycle = 900
   while 1:
    time.sleep(0.001)
   # I suspect the read/write to the GPIO is expensive and this is why the device crashes....
   # Process RED led's modes

    if (redledmode == 0):
#      GPIO.output('PA11', GPIO.LOW)
       setRedLed(0)
    if (redledmode == 1):
#      GPIO.output('PA11', GPIO.HIGH)
       setRedLed(1)
    if (redledmode == 2):
      # flash LED on and off at 1Hz
      if (redledtoggle == 0):
        redledcycle=redledcycle-1
        if (redledcycle == 0):
          redledcycle=500
          redledtoggle=1 
#          GPIO.output('PA11', GPIO.HIGH)
          setRedLed(1)
      if (redledtoggle == 1):
        redledcycle=redledcycle-1
        if (redledcycle == 0):
          redledcycle=500
          redledtoggle=0
#          GPIO.output('PA11', GPIO.LOW)
          setRedLed(0)
#
    if (redledmode == 3):
       # flash LED on and off at 1/9 duty
      if (redledtoggle == 0):
        redshortcycle=redshortcycle-1
        if (redshortcycle == 0):
          redshortcycle=100
          redledtoggle=1
          setRedLed(0)
#          GPIO.output('PA11', GPIO.LOW)
      if (redledtoggle == 1):
        redlongcycle=redlongcycle-1
        if (redlongcycle == 0):
          redlongcycle=900
          redledtoggle=0
          setRedLed(1)
#          GPIO.output('PA11', GPIO.HIGH)

   #------------- Process GREEN led's modes ---------------------
    if (greenledmode == 0):
#      GPIO.output('PA12', GPIO.LOW)
      setGreenLed(0)
    if (greenledmode == 1):
      setGreenLed(1)
#      GPIO.output('PA12', GPIO.HIGH)

    if (greenledmode == 2):
      # flash LED on and off at 1Hz
      if (greenledtoggle == 0):
        greenledcycle=greenledcycle-1
        if (greenledcycle == 0):
          greenledcycle=500
          greenledtoggle=1
          setGreenLed(1)
#          GPIO.output('PA12', GPIO.HIGH)
      if (greenledtoggle == 1):
        greenledcycle=greenledcycle-1
        if (greenledcycle == 0):
          greenledcycle=500
          greenledtoggle=0
          setGreenLed(0)
#          GPIO.output('PA12', GPIO.LOW)

    if (greenledmode == 3):
       # flash LED on and off at 1/9 duty
      if (greenledtoggle == 0):
        greenshortcycle=greenshortcycle-1
        if (greenshortcycle == 0):
          greenshortcycle=100
          greenledtoggle=1
          setGreenLed(0)
#          GPIO.output('PA12', GPIO.LOW)
      if (greenledtoggle == 1):
        greenlongcycle=greenlongcycle-1
        if (greenlongcycle == 0):
          greenlongcycle=900
          greenledtoggle=0
          setGreenLed(1)
#          GPIO.output('PA12', GPIO.HIGH)

# Initialise the SUNXI GPIO
GPIO.setmode(GPIO.SUNXI)
GPIO.setwarnings(False)
GPIO.setup('PA12', GPIO.OUT)  # green LED
GPIO.setup('PA11', GPIO.OUT)  # red LED


# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ensure that you can restart your server quickly when it terminates
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set the client socket's TCP "well-known port" number
well_known_port = 8881
sock.bind(('', well_known_port))

# Set the number of clients waiting for connection that can be queued
sock.listen(5)

# By default, we turn on the green LED to emulatle the way the Seagate Central used to work
greenledmode = 1

# start the LED control thread
x = threading.Thread(target=led_control_thread, args=())
x.start()

# loop waiting for connections (terminate with Ctrl-C)
try:
    while 1:
        newSocket, address = sock.accept(  )
        #print ("Connected from", address)
        # loop serving the new client
        while 1:
            receivedData = newSocket.recv(1024)
            if not receivedData: break
            # Print the data we got
            #print ("Data rcv'd: ", receivedData)
            commandURL = receivedData.decode('utf-8')
            if 'GET' in commandURL:
               if 'RedLED=ON' in commandURL:
                  redledmode=1
               if 'RedLED=OFF' in commandURL:
                  redledmode=0
               if 'RedLED=FLASH50' in commandURL:
                  redledmode=2
               if 'RedLED=FLASH10' in commandURL:
                  redledmode=3 
               if 'GreenLED=ON' in commandURL:
                  greenledmode=1
               if 'GreenLED=OFF' in commandURL:
                  greenledmode=0
               if 'GreenLED=FLASH50' in commandURL:
                  greenledmode=2
               if 'GreenLED=FLASH10' in commandURL:
                  greenledmode=3


            if 'POST' in commandURL:
               if 'RedLED=ON' in commandURL:
                  redledmode=1
               if 'RedLED=OFF' in commandURL:
                  redledmode=0
               if 'RedLED=FLASH50' in commandURL:
                  redledmode=2
               if 'RedLED=FLASH10' in commandURL:
                  redledmode=3
               if 'GreenLED=ON' in commandURL:
                  greenledmode=1
               if 'GreenLED=OFF' in commandURL:
                  greenledmode=0
               if 'GreenLED=FLASH50' in commandURL:
                  greenledmode=2
               if 'GreenLED=FLASH10' in commandURL:
                  greenledmode=3


            # Any command sent, we want to return HTTP 200 OK so the browser doesn't choke
            response = "HTTP/1.1 200 OK\r\n\r\n"
            r = response.encode('utf-8')
            newSocket.send(r)
            #print("Data Sent: ", r)
            break
            # newSocket.send(receivedData)
        newSocket.close(  )
        #print ("Disconnected from", address)
finally:
    sock.close(  )
