from flask import Flask
import os
import psycopg2

api_owm = os.environ['api_owm']
URL = {
    'DB':   os.environ['DATABASE_URL'],
    'BOT':  'https://api.telegram.org/bot' + os.environ['api_tg'] + '/',
    'STAT': 'http://api.openweathermap.org/data/2.5/weather?appid=' + api_owm,
    'SAT':  'http://sat.owm.io/sql/{}/{}/{}?from=cloudless&appid=' + api_owm,
    'WMAP': 'https://tile.openweathermap.org/map/{}_new/{}/{}/{}.png?appid=' + api_owm,
    'MAP':  ''
}

app = Flask(__name__)

conn = psycopg2.connect(URL['DB'], sslmode='require')
conn.autocommit = True
cur = conn.cursor()

from app import run
