# import os
# from datetime import datetime
# import time
# filename = "C:/Users/halib/OneDrive/Desktop/keymousespeed01_alpha2_1/keymousespeed01_alpha2_1/keymousespeed01/bin/Debug/a_06282022165432.log"
# date_time = datetime.fromtimestamp( os.stat(filename).st_mtime ) 
# print(date_time)

# threshold = 20
# # active = time.time()
# # now = time.time()

# while True:
#     now = datetime.now()
#     if (now - datetime.fromtimestamp( os.stat(filename).st_mtime)).total_seconds() > threshold:
#         print('inactive!')
#     time.sleep(threshold)
# #     if (now - active) > threshold:
# #         print('Inactive for ', now-ACTIVE, 'seconds')

# #     before = current

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")