from flask import Flask, request, render_template
import requests

mychat = 571267260
API_KEY = '694985196:AAFoZWhhsDF4qyvj0bJQNjn89PZypztg3Xc'
BOT_URL = 'https://api.telegram.org/bot' + API_KEY + '/'
weathertxt = 'Temperatuur: {} C\nWind: {} m/s\nRegenkans: {}%'

app = Flask(__name__)

def send_message(chat_id, text):
    url = BOT_URL + 'sendMessage'
    data = {'chat_id':chat_id, 'text':text}
    requests.post(url, json=data)

def getweather(loc):
    if isinstance(loc, dict):
        loc = str(loc['latitude'])+','+str(loc['longitude'])
    url = 'https://weerlive.nl/api/json-10min.php?locatie=' + loc
    data = requests.get(url,timeout=10).json()['liveweer'][0]
    response = weathertxt.format(data['temp'],data['windms'],data['d0neerslag'])
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if 'message' in data:
        data = data['message']
        chat = data['chat']['id']
        if 'location' in data:
            text = getweather(data['location'])
        elif 'text' in data:
            text = getweather(data['text'])

    send_message(chat,text)
    return ''
