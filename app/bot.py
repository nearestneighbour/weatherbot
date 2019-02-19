from app import app, BOT_URL
from app.weather import getweather
#from wiki import getwiki

from flask import request, render_template
import requests

def send_message(chat_id, text):
    url = BOT_URL + 'sendMessage'
    data = {'chat_id':chat_id, 'text':text}
    requests.post(url, json=data)

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
