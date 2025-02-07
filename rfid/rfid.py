'''RFID employee card reading and send mqtt''' 

import numpy as np
import time
import threading
import paho.mqtt.publish as publish
import evdev

from evdev import InputDevice, categorize, ecodes


def rfidRead():
  '''rfid reader empno card'''

  #mapping values
  RFID_LOOKUP = {
	2: '1',
	3: '2',
	4: '3',
	5: '4',
	6: '5',
	7: '6',
	8: '7',
	9: '8',
	10: '9',
        11: '0',
        28:'enter'
  }
  
  #find device
  #devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
  #for device in devices:
      #print(device.path, device.name, device.phys)

  #reader code
  code = ''
  dev = InputDevice('/dev/input/event0') #device input
  
  #looping read
  for event in dev.read_loop():
      if event.type == ecodes.EV_KEY:
          raw = str(categorize(event))
          splits = raw.split(', ')
          if str(splits[2]) == 'down':
              x = splits[1].split(' ')[0]
              num = RFID_LOOKUP[int(x)]
              code = code+num      
              if num == 'enter':  
                  code = code[:-5]
                  if len(code) != 10:
                      code = 'card reader error'
                      print(code)
                  else:
                      global rfid
                      rfid = code                           
                      print(rfid) 
 
                      # send mqtt to nodered
                      ret = publish.single("Rfid/CardNo", 
                            rfid, hostname="192.168.100.3")

                  #clear 
                  code = ''


def thread_rfid():
  '''thrading for rfid'''
  return rfidRead()


if __name__ == '__main__':

  #start threading rfid
  thrrfid = threading.Thread(target=thread_rfid) 
  thrrfid.start()

  #find device
  devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
  for device in devices:
      print(device.path, device.name, device.phys)