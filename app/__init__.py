from flask import Flask
import os
import psycopg2

w_api = os.environ['weatherapi']
URL = {
    'DB':   os.environ['DATABASE_URL'],
    'BOT':  'https://api.telegram.org/bot' + os.environ['apikey'] + '/',
    'STAT': 'http://api.openweathermap.org/data/2.5/weather?appid=' + w_api,
    'MAP':  'http://sat.owm.io/sql/{}/{}/{}?from=cloudless&appid=' + w_api,
    'WMAP': 'https://tile.openweathermap.org/map/{}_new/{}/{}/{}.png?appid=' + w_api
}

app = Flask(__name__)

conn = psycopg2.connect(URL['DB'], sslmode='require')
conn.autocommit = True
cur = conn.cursor()

from app import run
