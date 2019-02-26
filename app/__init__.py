from flask import Flask
import os
import psycopg2

# move to weather package __init__()
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

conn = psycopg2.connect(URL['DB'], sslmode='require')
conn.autocommit = True
cur = conn.cursor()

from app import run
