import requests
from datetime import datetime
get_heights_url = 'https://desks.medien.ifi.lmu.de/heights/id'

header = {'Content-Type': 'application/json; charset=utf-8'}

active_users = []
for i in range(0,20):
    heights_json = {"userid": i, "time": "2022-07-27 00:00:00"}
    response = requests.get(get_heights_url, json=heights_json, headers=header)
    heights = response.json()
    created = []
    if len(heights) > 0:
        active_users.append(i)
        for height in heights:
            date = datetime.strptime(height['created'], '%a, %d %b %Y %H:%M:%S %Z')
            if date.day not in created:
                created.append(date.day)
    
        print ("User number: ", i, "was active for ", len(created), " days")
        print(created)


print("There were ", len(active_users), "active users")