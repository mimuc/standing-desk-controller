# This file is a lambda that checks for user activity in the past hour on the server and sends a STAND command to any 
# desks where the user has not stood for at least one minute within the hour

import requests
import time
from datetime import datetime, timedelta
import json

time_threshold = 60
standing_threshold = 1000

get_heights_url = 'http://141.84.8.105:5000/heights'
time_filter = datetime.utcnow() - timedelta(seconds=time_threshold)
filter = [dict(name='time', op='eq', val=1655315165000)]
params = dict(q=json.dumps(dict(filters=filter)))

post_commands_url = 'http://141.84.8.105:5000/commands/add'
header = {'Content-Type': 'application/json; charset=utf-8'}



response = requests.get(get_heights_url, params=params, headers=header)
responseJson = response.json()
print(len(responseJson))
print(responseJson[-1]['time'])
print(time.time())

if(len(responseJson) > 0):
    lastTime = responseJson[-1]['time']
    lastHeight = responseJson[-1]['height']
    lastDate = datetime.strptime(responseJson[-1]['created'], '%Y-%m-%d %H:%M:%S')

    now = int(1000*time.time())
    currentTime = datetime.utcnow()

    print('lastDate: ', lastDate)
    print('currentDate: ', currentTime)

    # If there are no heights in the last (time_threshold) amount of time, check the height
    if ((currentTime - lastDate).total_seconds() > time_threshold):
        print(f'no new heights in {time_threshold} seconds')
        # if the last height is sitting, this means the user has been sitting for the whole time threshold
        # so send stand command
        if (lastHeight < standing_threshold):
            command_json = {'command': responseJson[-1]['standkey'], 'userid': responseJson[-1]['userid']}
            print('posting')
            # response = requests.post(post_commands_url, json = command_json, headers=header)
            # print(response)
        else:
            print('Already standing')
    # If there are heights recorded within the time threshold, check to see if the user has stood
    else:
        print('Heights too recent')
else:
    print('No heights')
