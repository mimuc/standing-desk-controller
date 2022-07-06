# This file is a lambda that checks for user activity in the past hour on the server and sends a 
# STAND command to any desks dependent on their experimental condition


import requests
from datetime import datetime, timedelta

## First set up variables that are used for all modes

time_threshold_second = 3000 # checks for the last 50 minutes at each XX:50
standing_threshold = 900 # above this counts as standing

now = (datetime.utcnow())
time_threshold = (now - timedelta(seconds=time_threshold_second)).strftime("%Y-%m-%d %H:%M:%S")


get_users_url = 'http://141.84.8.105:5000/users/condition'
get_heights_url = 'http://141.84.8.105:5000/heights/id'
post_commands_url = 'http://141.84.8.105:5000/commands/add'
header = {'Content-Type': 'application/json; charset=utf-8'}

# This one only cares about users in condiiton A (apple watch style)
users_json_a = {'condition': 'A'}
# This one only cares about users in condiiton R (regular intervals)
users_json_r = {'condition': 'R'}


def send_post_command(command_json):
        print('posting')
        response = requests.post(post_commands_url, json=command_json, headers=header)
        print(response)

        
def run():

    ############ First, fetch all users who are in the R condition (regular interval mode) ##################
    print('Running R condition')
    response = requests.get(get_users_url, json=users_json_r, headers=header) # test version with no filter
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

    
    ############### Second do the A condition (apple watch style) ################
    print('Running A condition')
    response = requests.get(get_users_url, json=users_json_a, headers=header) # test version with no filter
    users = response.json()
    print('Users: ', users)

    # If there are any users in this condition, keep going
    if(len(users) > 0):
        # loop through each user in the database
        for user in users:
            # Check if they are in the active week (timeline is 1 week manual, 1 week active, 1 week manual)
            started_time = datetime.strptime(user['startdate'], '%Y-%m-%d %H:%M:%S')
            experiment_day = (now - started_time).days
            if (experiment_day >=7) and (experiment_day <14):
                # Prep height json and command json for this user
                heights_json = {'userid': user['userid'], 'time': str(time_threshold)}
                command_json = {'command': user['standkey'], 'userid': user['userid']}

                # get all heights for this user more recent than time_threshold
                response = requests.get(get_heights_url, json=heights_json, headers=header)
                heights = response.json()

                

                # If there are heights, more checks required
                if (len(heights) > 0):
                    stand_flag = 0
                    # check if the user has stood this hour
                    for height in heights:
                        if (height['height'] > standing_threshold):
                            stand_flag = 1
                    # if no flag, the user has not stood this hour
                    if stand_flag == 0:
                        send_post_command(command_json)
                    # if they already stood this hour, do nothing
                    else:
                        print('User already stood this hour')
                # If there are no heights at all, send stand command  
                else:
                    print('no heights')
                    send_post_command(command_json)
            # If they are not within the active week, do nothing
            else:
                print ("Not in active A condition, currently on day ", experiment_day)
    else:
        print('No users')

