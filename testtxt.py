import requests as r

url = 'http://0.0.0.0:5000/tgbot'
#url = 'http://127.0.0.1:8000/tgbot'
#url1 = 'https://api.telegram.org/bot694985196:AAFoZWhhsDF4qyvj0bJQNjn89PZypztg3Xc/sendMessage?chat_id=571267260'
#url2 = 'https://webhook.site/f78a9de3-e653-42f2-89ec-e8d05b5c3fbe'

#data = {'message':{'chat':{'id':571267260},'location':{'latitude':51.84,'longitude':5.86}}}
data = {'message':{'chat':{'id':571267260},'text':'location Nijmegen'}}

r.post(url, json=data)
