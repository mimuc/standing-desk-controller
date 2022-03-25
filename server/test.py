import requests
import random

url = 'http://127.0.0.1:5005/addhight'
for x in range (10):
	myobj = {'userid': 1, 'hight': round(random.uniform(72, 120), 1)}
	x = requests.post(url, json = myobj)

print(x.text)