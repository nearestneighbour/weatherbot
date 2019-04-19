from flask import Flask, request
import os

from app import sql

API = {
    'TG': os.environ['api_tg'],
    'OWM': os.environ['api_owm'],
    'HEREID': os.environ['here_appid'],
    'HEREC': os.environ['here_appc']
}
URL = {
    'DB':   os.environ['DATABASE_URL'],
    'BOT':  'https://api.telegram.org/bot' + API['TG'] + '/',
    'STAT': 'http://api.openweathermap.org/data/2.5/weather?appid=' + API['OWM'],
    'MAP':  'https://image.maps.api.here.com/mia/1.6/mapview?app_id={}&app_code={}&nodot'
    .format(API['HEREID'],API['HEREC']),
    'WMAP': 'https://tile.openweathermap.org/map/{}_new/{}/{}/{}.png?appid=' + API['OWM']
    #'SAT':  'http://sat.owm.io/sql/{}/{}/{}?from=cloudless&appid=' + api_owm,
    #'MAP':  'https://a.tile.openstreetmap.org/{}/{}/{}.png'
}
app = Flask(__name__)
db = sql.sql(URL['DB'])

from app import weatherbot

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return 'no data'
    elif 'message' in data:
        weatherbot.process_msg(data['message'])
        return ''
