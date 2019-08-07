import os
DB_URL = os.environ['DATABASE_URL']
API_OWM = os.environ['api_owm']
HERE_ID = os.environ['here_appid']
HERE_CODE = os.environ['here_appc']
URL_TG = os.environ['url_tg']

from flask import Flask, request
app = Flask(__name__)

from .weatherbot import process_msg

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return 'no data'
    elif 'message' in data:
        process_msg(data['message'])
        return ''
