from flask import Flask, request
import requests

app = Flask(__name__)
weathermsg = 'Temperatuur: {} C\nWind: {} m/s\nRegenkans: {}%'

def send_message(prepared_data):
    message_url = 'https://api.telegram.org/bot694985196:AAFoZWhhsDF4qyvj0bJQNjn89PZypztg3Xc/sendMessage'
    requests.post(message_url, json=prepared_data)

def getweather(location):
    url = 'https://weerlive.nl/api/json-10min.php?locatie='+location
    data = requests.get(url,timeout=10).json()['liveweer'][0]
    return data

@app.route('/hello')
def hello_world():
    return 'Hello, World!12'

@app.route('/txt', methods=['GET','POST'])
def getmsg():
    if request.method == 'GET':
        if 'chat_id' not in request.args:
            return "empty get request"
        chat_id = request.args['chat_id']
        txt = request.args['text']
        vv = 'get'
    elif request.method == 'POST':
        data = request.get_json()
        if 'message' in data:
            msg = data['message']
            chat_id = msg['chat']['id']
            if 'location' in msg:
                location = str(msg['location']['latitude'])+','+str(msg['location']['longitude'])
                weather = getweather(location)
                txt = weathermsg.format(weather['temp'],weather['windms'],weather['d0neerslag'])
                vv = 'loc'
            elif 'text' in msg:
                txt = msg['text'][::-1]
                vv = 'rev'
    send_message({'chat_id':chat_id,'text':txt})
    return vv
