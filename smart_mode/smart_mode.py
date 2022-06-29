import os
from datetime import datetime
import time
filename = "C:/Users/halib/OneDrive/Desktop/keymousespeed01_alpha2_1/keymousespeed01_alpha2_1/keymousespeed01/bin/Debug/a_06282022165432.log"
date_time = datetime.fromtimestamp( os.stat(filename).st_mtime ) 
print(date_time)

threshold = 20
# active = time.time()
# now = time.time()

while True:
    now = datetime.now()
    if (now - datetime.fromtimestamp( os.stat(filename).st_mtime)).total_seconds() > threshold:
        print('inactive!')
    time.sleep(threshold)
#     if (now - active) > threshold:
#         print('Inactive for ', now-ACTIVE, 'seconds')

#     before = current