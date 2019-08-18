import os
DB_URL = os.environ['DATABASE_URL']
OWM_API = os.environ['owm_api']
HERE_APP_ID = os.environ['here_appid']
HERE_APP_CODE = os.environ['here_appc']
TG_URL = os.environ['tg_url']

from flask import Flask, request
app = Flask(__name__)

from .sql import sql
db = sql(DB_URL)

from .weatherbot import process_msg

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return 'no data'
    elif 'message' in data:
        process_msg(data['message'])
        return ''
