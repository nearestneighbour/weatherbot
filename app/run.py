from app import app, URLS
from app.bot import tgbot
#from app.weather import getweather

from flask import request, render_template
import requests
import psycopg2
import os

DB_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DB_URL, sslmode='require')

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return ''
    if 'message' in data:
        msg = data['message']
        chat_id = msg['chat']['id']
        if chat_id in botlist:
            botlist[chat_id].process_msg(msg)
        else:
            botlist[chat_id] = tgbot(chat_id, msg)
    return ''

@app.route('/')
def index():
    return render_template('index.html')
