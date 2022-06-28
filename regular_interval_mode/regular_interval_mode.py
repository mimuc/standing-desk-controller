# This file is a lambda that simply tells the desk to enter standing mode once per hour
# the code is evoked 10 minutes before the hour each working hour (9-17)

import requests
from datetime import datetime


now = (datetime.utcnow())

get_users_url = 'http://141.84.8.105:5000/users/condition'
post_commands_url = 'http://141.84.8.105:5000/commands/add'
header = {'Content-Type': 'application/json; charset=utf-8'}

# This lambda only cares about users in condiiton R (regular intervals)
users_json = {'condition': 'R'}


# First, fetch all users who are in the R condition (regular interval mode)
response = requests.get(get_users_url, json=users_json, headers=header) # test version with no filter
users = response.json()
print(users)


# If there are any users in this condition, check if they are in the active portion
if(len(users) > 0):
    # loop through each user in the database
    for user in users:
        # Check if they are in the active week (timeline is 1 week manual, 1 week active, 1 week manual)
        started_time = datetime.strptime(user['startdate'], '%Y-%m-%d %H:%M:%S')
        experiment_day = (now - started_time).days
        if (experiment_day >=7) and (experiment_day <14):
            # Create the command post request
            command_json = {'command': user['standkey'], 'userid': user['userid']}
            # Post standing command to database for each user
            response = requests.post(post_commands_url, json=command_json, headers=header)
            print('posting')
        # If they are not within the active week, do nothing
        else:
            print ("Not in active R condition, currently on day ", experiment_day)
else:
    print('No users')
