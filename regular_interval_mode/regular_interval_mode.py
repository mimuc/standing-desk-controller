# This file is a lambda that simply tells the desk to enter standing mode once per hour
# the code is evoked 10 minutes before the hour each working hour (9-17)

import requests
import time
from datetime import datetime, timedelta
import json

now = (datetime.now())
# now = datetime.now() + timedelta(days=13) # test version

get_users_url = 'http://141.84.8.105:5000/users/condition'
post_commands_url = 'http://141.84.8.105:5000/commands/add'
header = {'Content-Type': 'application/json; charset=utf-8'}

# This lambda only cares about users in condiiton R (regular intervals)
users_json = {'condition': 'R'}


# First, fetch all users who are in the R condition (regular interval mode)
# response = requests.get(get_users_url, params=params, headers=header)
response = requests.get(get_users_url, json=users_json, headers=header) # test version with no filter
responseJson = response.json()
print(responseJson)


# If there are any users in this condition, check if they are in the active portion
if(len(responseJson) > 0):
    # loop through each user in the database
    for user in responseJson:
        # Check if they are in the active week (timeline is 1 week manual, 1 week active, 1 week manual)
        created_time = datetime.strptime(responseJson[-1]['created'], '%Y-%m-%d %H:%M:%S')
        experiment_day = (now - created_time).days
        if (experiment_day >=7) and (experiment_day <14):
            # Create the command post request
            command_json = {'command': user['standkey'], 'userid': user['userid']}
            # Post standing command to database for each user
            response = requests.post(post_commands_url, json=command_json, headers=header)
            print('posting')
        else:
            print ("Not in active R condition, currently on day ", experiment_day)
else:
    print('No users')
