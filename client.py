import requests
from const import *

base_url = 'http://' + BROKER_ADDR + ':5000'

response = requests.get(base_url + '/latest')
data = response.json()
print('Latest average: ' + str(data['average']) + ' at ' + data['timestamp'])

response = requests.get(base_url + '/history')
history = response.json()
print('History:')
for entry in history:
    print('  ' + str(entry['average']) + ' at ' + entry['timestamp'])
