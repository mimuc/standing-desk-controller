import requests
from datetime import datetime
import pandas as pd

get_heights_url = 'https://desks.medien.ifi.lmu.de/heights/id'

user_startdates = { 
    0: 'no',
    1: 'no',
    2: '2022-07-27',
    3: '2022-07-27',
    4: '2022-07-28',
    5: 'no',
    6: '2022-08-11',
    7: '2022-08-12',
    8: '2022-08-17',
    9: 'no',
    10: '2022-08-11',
    11: '2022-07-28',
    12: '2022-07-27',
    13: 'no',
    14: 'no',
    15: 'no',
    16: 'no',
    17: 'no',
    18: 'no',
    19: 'no',
    20: 'no',
    21: '2022-08-24',
    22: '2022-08-24',
    23: '2022-08-24',
    24: '2022-08-24',
    25: '2022-08-24',
    26: '2022-08-24',
    27: '2022-09-26',
    28: '2022-09-28'
}

header = {'Content-Type': 'application/json; charset=utf-8'}

df = pd.DataFrame(columns = ['ID', 'Timestamp', 'Height'])

active_users = []
for i in range(0,29):
    print('user ', i)
    heights_json = {"userid": i, "time": user_startdates[i]}
    if user_startdates[i] != 'no':
        response = requests.get(get_heights_url, json=heights_json, headers=header)
    else:
        print('no real user number ', i)
        continue
    heights = response.json()
    
    created = []
    incondition = []
    if len(heights) > 0:
        active_users.append(i)
        for height in heights:

            date = datetime.strptime(height['created'], '%a, %d %b %Y %H:%M:%S %Z')
            # temp = pd.DataFrame(data={'ID': [height['userid']], 'Timestamp': [date], 'Height': [height['height']]})
            # df = pd.concat([df, temp])
            if date.day not in created:
                created.append(date.day)
            if (date - datetime.strptime(user_startdates[i], '%Y-%m-%d')).days >= 7 and date.day not in incondition:
                incondition.append(date.day)


        # print ("User number: ", i, "was active for ", len(created), " total days")
        print ("User number: ", i, "was active for ", len(incondition), " condition days")
        print ("User number: ", i, "was active for ", len(created) - len(incondition), " manual days")
        print(created)
        print(incondition)


print("There were ", len(active_users), "active users")
# df.to_csv('heights.csv', header=True)