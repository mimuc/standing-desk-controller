# This file is a lambda that simply tells the desk to enter standing mode once per hour
# the code is evoked 10 minutes before the hour each working hour (9-17)

import requests
import time
from datetime import datetime, timedelta
import json



get_users_url = 'http://141.84.8.105:5000/users'

# TODO make this filter by MODE (i.e. regular interval mode)
filter = [dict(name='time', op='eq', val=1655315165000)] 
params = dict(q=json.dumps(dict(filters=filter)))

post_commands_url = 'http://141.84.8.105:5000/commands/add'
header = {'Content-Type': 'application/json; charset=utf-8'}


# First, fetch all users who are in the R condition (regular interval mode)
# response = requests.get(get_users_url, params=params, headers=header)
response = requests.get(get_users_url, headers=header)
responseJson = response.json()
print(responseJson)

# If there are any users in this condition, initiate standing
if(len(responseJson) > 0):
    # loop through each user in the database
    for user in responseJson:
        # Create the command post request
        command_json = {'command': user['standkey'], 'userid': user['userid']}
        # Post standing command to database for each user
        response = requests.post(post_commands_url, json = command_json, headers=header)
else:
    print('No users')
