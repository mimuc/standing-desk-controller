# Wi-Fi AP Mode Example
#
# This example shows how to use Wi-Fi in Access Point mode.
# this version by Albrecht Schmidt, https://www.sketching-with-hardware.org/wiki/
# based on the following examples:
# https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
# https://docs.arduino.cc/tutorials/nano-rp2040-connect/rp2040-python-api


import network, socket, time
from machine import UART, Pin
import ubinascii

import urequests as requests
import json
# from netvars import setNetVar, getNetVar, initNet
import _thread


# For threading
# S = Semaphore(16)


ssid = "HCUM"
passwd = "wearedoingresearch."

# # assuming there is a network with ssid hotspot1 and password 123456789
# connect to wifi
def connectToWifi(ssid, passwd):
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(ssid, passwd)
        while not wlan.isconnected():
            pass
    
        print('network config:', wlan.ifconfig())
        return wlan
    except:
        return connectToWifi(ssid, passwd)
    
wlan = connectToWifi(ssid, passwd)

# IPv4 address
serverUrl = 'http://10.163.181.50:5000/heights/add'
# serverUrl = 'http://127.0.0.1:5000/heights/add'


d0 = Pin(25, Pin.OUT)              #D0, up signal
d1 = Pin(15, Pin.OUT)              #D1, down signal
d2 = Pin(16, Pin.OUT)              #D2, preset 2 signal
d3 = Pin(17, Pin.OUT)              #D3, M signal

d0in = Pin(13, Pin.IN)              #D0, up signal
d1in = Pin(12, Pin.IN)              #D1, down signal

# set all pins to high (high = inactive)
d0.value(0)
d1.value(0)
d2.value(0)
d3.value(0)



Rx = bytearray(8)
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1)                         # init with given baudrate


# SSID ='Nano_RP2040_Connect_test'   # Network SSID
# KEY  ='12345678'                 # Network key (should be 8 chars) - for real use, choose a safe one
HOST = ''
PORT = 80                          # 80 ist the http standard port, can also use non-privileged port e.g. 8080
# 
# # Init wlan module and connect to network
# wlan = network.WLAN(network.AP_IF)
# wlan.active(True)
# # it seems in this version the AP mode only supports WEP
# wlan.config(essid=SSID, key=KEY, security=wlan.WEP, channel=2)

# print("AP mode started. SSID: {} IP: {}".format(SSID, wlan.ifconfig()[0]))
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print("mac address: ", mac)




def post_request(req_data):
#     try:
    global serverUrl
    #print(_thread.get_ident())
    header = {'Content-Type': 'application/json; charset=utf-8'}
    r = requests.post(serverUrl, json=req_data, headers=header)
    print(r.json())
    r.close()
#     except Exception as e:
#         global buffer
#         buffer.append(req_data)
#         print("T Done with error", e)
#         time.sleep(1)
#         isDoneThread = True
#         _thread.exit()
        
        

buffer =[]
lastHeight = -1      
# loop to deal with  http requests
while True:
  #for i in range(0,100):
  uart.readinto(Rx)         # read all available characters
  flag1=0
  flag2=0
  flag3=0
  a=0
  b=0
  for x in Rx:
    if (x == 1 and flag1 == 0):
      flag1=1
    elif (x == 1 and flag1 == 1):
      flag2=1
    elif (flag1 == 1 and flag2 == 1 and a==0):
      a=x
    elif (flag1 == 1 and flag2 ==1 and flag3 == 0):
      b=x
      flag3=1
  Rx=bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')
      
  #print(int(a), int(b), len(buffer))
  # Start sending when idle
  if ((int(a) == 0) & (int(b)==0) & (len(buffer) > 1) & (wlan.isconnected())):
      lstHeight = []
      lstTime = []
      for e in buffer:
          lstHeight.append(e["height"])
          lstTime.append(e["time"])
      if (len(lstHeight) > 0):
          #print(a, b, len(buffer))
          post_data = {'macaddress': mac,
                        'heights': lstHeight,
                        'times': lstTime
                        }
          try:
              post_request(post_data)
              buffer = []
          except Exception as e:
              print("Exception", str(e))
              time.sleep(0.1)
              buffer.append(post_data)
     

  #print(a, b)          
  currentHeight = a*256+b
  if ((lastHeight != currentHeight) & (int(a) != 0) & (int(b) != 0)):
          
      print("height:", currentHeight)
      post_data = {'macaddress': mac,
                    'height': currentHeight,
                    'time': int(1000*time.time())
                    }
      
      buffer.append(post_data)

      lastHeight = currentHeight
      
  if not wlan.isconnected():
      wlan = connectToWifi(ssid, passwd)


