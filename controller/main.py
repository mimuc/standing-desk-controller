# This code operates an Arduino Nano RP2040 connected to a custom
# Circuit board to control a standing desk based on commands sent
# to a central server.
# Created by Luke Haliburton, Sven Mayer, and Albrecht Schmidt
# At LMU Munich, 2022

import network, socket, time
from machine import UART, Pin
import machine
import ubinascii
import urequests as requests
import json
import gc
from sys import platform


gc.collect()

# Set Device Name and Version Number
versionNumber = "0.03"
mac = "Ares"
print("mac address: ", mac)


# Hard coded wifi name and password
ssid = "HCUM"
passwd = "wearedoingresearch."


# assuming there is a network with ssid and passwd
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
        time.sleep(2)
        return connectToWifi(ssid, passwd)
    
wlan = connectToWifi(ssid, passwd)

# IPv4 address
# Change this based on the address of the server
serverUrl_postAlive = 'http://desks.medien.ifi.lmu.de/startupLogger/add'
serverUrl_postHeight = 'http://desks.medien.ifi.lmu.de/heights/add'

serverUrl_getCommand = 'http://desks.medien.ifi.lmu.de/commands/mac'


# These pins correspond with the custom PCB to control the desk
d0 = Pin(25, Pin.OUT)              #D0, up signal
d1 = Pin(15, Pin.OUT)              #D1, down signal
d2 = Pin(16, Pin.OUT)              #D2, preset 2 signal
d3 = Pin(17, Pin.OUT)              #D3, M signal

d0in = Pin(13, Pin.IN)              #D0, up signal
d1in = Pin(12, Pin.IN)              #D1, down signal

# set all pins to inactive
d0.value(0)
d1.value(0)
d2.value(0)
d3.value(0)


# init UART pin with given baudrate to read the height of the desk
Rx = bytearray(8)
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1)                         






# This function interprets a command fetched from the server and activates the
# indicated button. For now, this only works with buttons 1-4, the preset height buttons
def execute_command(newCommand):
#     print('New command: ', newCommand)
    if newCommand:
        if (newCommand <=4):
            # simulate a button press (1 through 4)
            if(newCommand == 1):
                print('Virtually pressed button 1')
                d0.value(1)
                d1.value(1)
                time.sleep(15)
                d0.value(0)
                d1.value(0)
            elif(newCommand == 2):
                print('Virtually pressed button 2')
                d2.value(1)
                time.sleep(15)
                d2.value(0)
            elif(newCommand == 3):
                print('Virtually pressed button 3')
                d1.value(1)
                d2.value(1)
                time.sleep(15)
                d1.value(0)
                d2.value(0)
            elif(newCommand == 4):
                print('Virtually pressed button 4')
                d0.value(1)
                d2.value(1)
                time.sleep(15)
                d0.value(0)
                d2.value(0)
            
        else:
            # go to a specific height and then stop
            print('New command is not a preset: ', newCommand)
#     else:
#         print('No commands')
    

# This function posts a request to the server. The request "req_data"
# should be in json format
def post_request(req_data, serverUrl_post=serverUrl_postHeight):
    serverUrl_post
    global wlan
    header = {'Content-Type': 'application/json; charset=utf-8'}
    try:
        r = requests.post(serverUrl_post, json=req_data, headers=header)
        
        rJson = r.json()
        r.close()
        return True
    except Exception as PostException:
        print('POST exception: ', PostException)
        machine.reset()
        
    


# This function fetches a request from the server. The request "req_data"
# should be in json format
def get_request(req_data, serverUrl_get=serverUrl_getCommand):
    serverUrl_get
    global wlan
    header = {'Content-Type': 'application/json; charset=utf-8'}
    try:
        r = requests.get(serverUrl_get, json=req_data, headers=header)
        rJson = r.json()
        r.close()
        if (rJson['status'] == 'success'):
            # if there is a command, execute it
            execute_command(rJson['command'])
    except Exception as GetException:
        print('GET exception: ', GetException)
        machine.reset()
    

class WDT:
    def __init__(self, timeout=120, use_rtc_memory=True):
        self._timeout = timeout / 10
        self._counter = 0
        self._timer = machine.Timer()
        self._use_rtc_memory = use_rtc_memory
        self.init()
        try:
            with open("watchdog.txt", "r") as f:
                if f.read() == "True":
                    print("Reset reason: Watchdog")
        except Exception as e:
            print(e)  # file probably just does not exist
        try:
            with open("watchdog.txt", "w") as f:
                f.write("False")
        except Exception as e:
            print("Error saving to file: {!s}".format(e))
            if use_rtc_memory and platform == "rp2":
                rtc = machine.RTC()
                if rtc.memory() == b"WDT reset":
                    print("Reset reason: Watchdog")
                rtc.memory(b"")

    def _wdt(self, t):
        self._counter += self._timeout
        if self._counter >= self._timeout * 10:
            try:
                with open("watchdog.txt", "w") as f:
                    f.write("True")
            except Exception as e:
                print("Error saving to file: {!s}".format(e))
                if self._use_rtc_memory and platform == "esp8266":
                    rtc = machine.RTC()
                    rtc.memory(b"WDT reset")
            machine.reset()

    def feed(self):
        self._counter = 0

    def init(self, timeout=None):
        timeout = timeout or self._timeout
        self._timeout = timeout
        self._timer.init(period=int(self._timeout * 1000), mode=machine.Timer.PERIODIC, callback=self._wdt)

    def deinit(self):  # will not stop coroutine
        self._timer.deinit()   

last_time_get = time.time()
buffer =[]
lastHeight = -1

# ping the server on startup to say that this unit has just started
initial_post = {"macaddress": mac, "versionNumber": versionNumber}
response = post_request(initial_post, serverUrl_postAlive)

# Start the watchdog
wdt=WDT()

# main loop to deal with  http requests
while True:
    try:
        # feed the watchdog
        wdt.feed()
        
        # read all available characters
        uart.readinto(Rx)         
        flag1=0
        flag2=0
        flag3=0
        a=0
        b=0
        # This loop reads in the bytes
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
          

        # Start sending when idle
        if ((int(a) == 0) & (int(b)==0) & (len(buffer) > 1) & (wlan.isconnected())):
            lstHeight = []
            lstTime = []
            for e in buffer:
                lstHeight.append(e["height"])
                lstTime.append(e["heighttime"])
            if (len(lstHeight) > 0):
                post_data = {"macaddress": mac,
                            "heights": lstHeight,
                            "heighttimes": lstTime
                            }
                
                try:
                    # try posting the height to the server
                    r = post_request(post_data)
                    if r:
                        buffer = []
                except Exception as e:
                    print("Exception - ", str(e))
                    time.sleep(0.1)
         

      
        # convert bytes into a height in cm
        currentHeight = a*256+b
        # if the height has changed, append it to the buffer
        if ((lastHeight != currentHeight) & (int(a) != 0) & (int(b) != 0)):
            post_data = {"macaddress": mac,
                        "height": currentHeight,
                        "heighttime": int(time.time())
                        }
            buffer.append(post_data)

            lastHeight = currentHeight
          
        # if the desk is not moving, look for commands on the server
        if ((int(a) == 0) & (int(b)==0) & (len(buffer) == 0) & (wlan.isconnected()) & ((time.time() - last_time_get) >= 5) ):
            get_data = {"macaddress": mac}
            get_request(get_data)
            last_time_get = time.time()
#             print('Time: ', last_time_get)
        
        # in case the wifi disconnects, try reconnecting
        if not wlan.isconnected():
            wlan = connectToWifi(ssid, passwd)
    except Exception as MainException:
        print('Main exception: ', MainException)
        reset()



