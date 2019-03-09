from flask import Flask, request
import os, sys

API = {'TG': os.environ['api_tg']}
URL = {
    'DB':   os.environ['DATABASE_URL'],
    'BOT':  'https://api.telegram.org/bot' + API['TG'] + '/'
}

app = Flask(__name__)

from app import sql

db = sql.sql(URL['DB'])

from app import weather, wallet#, wiki

BOTS = {
    'weather': sys.modules['app.weather'],
    'wallet': sys.modules['app.wallet']
}

from app import tgbot

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return 'no data'
    elif 'message' in data:
        tgbot.process_msg(data['message'])
        return ''
