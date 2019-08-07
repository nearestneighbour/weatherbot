# In order to send test messages to the bot and monitor the response do the following:
# 1) On beeceptor.com create a new endpoint, keep tab open
# 2) In .env, set url_tg=URL from beeceptor
# 3) In bash, execute python3 test_local.py
# 4) Examine the responses that are shown in the browser

import requests

url = 'http://0.0.0.0:5000/tgbot'

# Change location using coordinates (corresponding to NYC)
data = {'message':{'chat':{'id':0},'location':{'latitude':40.71,'longitude':-74}}}
requests.post(url, json=data)

# Request location info
data = {'message':{'chat':{'id':0},'text':'location'}}
requests.post(url, json=data)

# Change location using city name
data = {'message':{'chat':{'id':0},'text':'location Albuquerque'}}
requests.post(url, json=data)

# Check weather in current location
data = {'message':{'chat':{'id':0},'text':'weather'}}
requests.post(url, json=data)

# Check weather in any location
data = {'message':{'chat':{'id':0},'text':'weather Athens'}}
requests.post(url, json=data)
