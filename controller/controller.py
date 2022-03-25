# Wi-Fi AP Mode Example
#
# This example shows how to use Wi-Fi in Access Point mode.
# this version by Albrecht Schmidt, https://www.sketching-with-hardware.org/wiki/
# based on the following examples:
# https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
# https://docs.arduino.cc/tutorials/nano-rp2040-connect/rp2040-python-api


import network, socket, time
from machine import Pin

d0 = Pin(25, Pin.OUT)              #D0, up signal
d1 = Pin(15, Pin.OUT)              #D1, down signal
d2 = Pin(16, Pin.OUT)              #D2, preset 2 signal
d3 = Pin(17, Pin.OUT)              #D3, M signal

# set all pins to high (high = inactive)
d0.value(1)
d1.value(1)
d2.value(1)
d3.value(1)



Rx = bytearray(8)

#uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1)                         # init with given baudrate


SSID ='Nano_RP2040_Connect_test'   # Network SSID
KEY  ='12345678'                 # Network key (should be 8 chars) - for real use, choose a safe one
HOST = ''
PORT = 80                          # 80 ist the http standard port, can also use non-privileged port e.g. 8080

# Init wlan module and connect to network
wlan = network.WLAN(network.AP_IF)
wlan.active(True)
# it seems in this version the AP mode only supports WEP
wlan.config(essid=SSID, key=KEY, security=wlan.WEP, channel=2)

print("AP mode started. SSID: {} IP: {}".format(SSID, wlan.ifconfig()[0]))


# create the webpage with a button to toggle the LED
def web_page():
  if d0.value() == 0 and d1.value() == 1 and d2.value() == 1:
    up_state="ON"
  else:
    up_state="OFF"
  if d0.value() == 1 and d1.value() == 0 and d2.value() == 1:
    down_state="ON"
  else:
    down_state="OFF"
  if d0.value() == 0 and d1.value() == 0:
    preset1_state="ON"
  else:
    preset1_state="OFF"
  if d0.value() == 1 and d1.value() == 1 and d2.value() == 0:
    preset2_state="ON"
  else:
    preset2_state="OFF"
  if d1.value() == 0 and d2.value() == 0:
    preset3_state="ON"
  else:
    preset3_state="OFF"
  if d0.value() == 0 and d2.value() == 0:
    preset4_state="ON"
  else:
    preset4_state="OFF"
  if d3.value() == 0:
    mbutton_state="ON"
  else:
    mbutton_state="OFF"
    
  
  html ="""<html><head>
      <title>Nano RP2040 Connnect Web Server</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="icon" href="data:,">
      </head>
      <body>
        <h1>Nano RP2040 Connnect </1>
        <h2>Web Server Test</h2>
        
        <p>Up state: <strong>""" + up_state + """</strong></p>
        <p><a href="/?up=on"><button class="button">ON</button></a></p>
        <p><a href="/?up=off"><button class="button button2">OFF</button></a></p>
        
        <p>Down state: <strong>""" + down_state + """</strong></p>
        <p><a href="/?down=on"><button class="button">ON</button></a></p>
        <p><a href="/?down=off"><button class="button button2">OFF</button></a></p>
        
        <p>Preset 1: <strong>""" + preset1_state + """</strong></p>
        <p><a href="/?preset1=on"><button class="button">ON</button></a></p>
        <p><a href="/?preset1=off"><button class="button button2">OFF</button></a></p>
        
        <p>Preset 2: <strong>""" + preset2_state + """</strong></p>
        <p><a href="/?preset2=on"><button class="button">ON</button></a></p>
        <p><a href="/?preset2=off"><button class="button button2">OFF</button></a></p>
        
        <p>Preset 3: <strong>""" + preset3_state + """</strong></p>
        <p><a href="/?preset3=on"><button class="button">ON</button></a></p>
        <p><a href="/?preset3=off"><button class="button button2">OFF</button></a></p>
        
        <p>Preset 4: <strong>""" + preset4_state + """</strong></p>
        <p><a href="/?preset4=on"><button class="button">ON</button></a></p>
        <p><a href="/?preset4=off"><button class="button button2">OFF</button></a></p>
        
        <p>Modify a Preset: <strong>""" + mbutton_state + """</strong></p>
        <p><a href="/?mbutton=on"><button class="button">ON</button></a></p>
        <p><a href="/?mbutton=off"><button class="button button2">OFF</button></a></p>
        
    
      </body>
      </html>"""
  return html

# get started with setting up the sever sockedt
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind and listen
server.bind([HOST, PORT])
server.listen(5)

# loop to deal with  http requests
while True:
  conn, addr = server.accept()
  print('Connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Request Content = %s' % request)
  # check if the request includes up=on or off
  up_on = request.find('/?up=on')
  up_off = request.find('/?up=off')
  # check if the request includes down=on or off
  down_on = request.find('/?down=on')
  down_off = request.find('/?down=off')
  # check if the request includes preset1=on or off
  preset1_on = request.find('/?preset1=on')
  preset1_off = request.find('/?preset1=off')
  # check if the request includes preset1=on or off
  preset2_on = request.find('/?preset2=on')
  preset2_off = request.find('/?preset2=off')
  # check if the request includes preset1=on or off
  preset3_on = request.find('/?preset3=on')
  preset3_off = request.find('/?preset3=off')
  # check if the request includes preset1=on or off
  preset4_on = request.find('/?preset4=on')
  preset4_off = request.find('/?preset4=off')
  # check if the request includes preset1=on or off
  mbutton_on = request.find('/?mbutton=on')
  mbutton_off = request.find('/?mbutton=off')
  # request is 'GET /?d0=on' or 'GET /?d0=off' - the string starts at position 6 (counting starts at 0)
  if up_on == 6:
    print('UP ON')
    d0.value(0)
  if up_off == 6:
    print('UP OFF')
    d0.value(1)
  if down_on == 6:
    print('DOWN ON')
    d1.value(0)
  if down_off == 6:
    print('DOWN OFF')
    d1.value(1)
  if preset1_on == 6:
    print('PRESET 1 ON')
    d0.value(0)
    d1.value(0)
  if preset1_off == 6:
    print('PRESET 1 OFF')
    d0.value(1)
    d1.value(1)
  if preset2_on == 6:
    print('PRESET 2 ON')
    d2.value(0)
  if preset2_off == 6:
    print('PRESET 2 OFF')
    d2.value(1)
  if preset3_on == 6:
    print('PRESET 3 ON')
    d1.value(0)
    d2.value(0)
  if preset3_off == 6:
    print('PRESET 3 OFF')
    d1.value(1)
    d2.value(1)
  if preset4_on == 6:
    print('PRESET 4 ON')
    d0.value(0)
    d2.value(0)
  if preset4_off == 6:
    print('PRESET 4 OFF')
    d0.value(1)
    d2.value(1)
  if mbutton_on == 6:
    print('MBUTTON ON')
    d3.value(0)
  if mbutton_off == 6:
    print('MBUTTON OFF')
    d3.value(1)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.send(response)
  conn.close()

