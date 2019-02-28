from flask import Flask
import os
import psycopg2

# move to weather package __init__()
API = {'TG': os.environ['api_tg']}
URL = {
    'DB':   os.environ['DATABASE_URL'],
    'BOT':  'https://api.telegram.org/bot' + API['TG'] + '/'
}

app = Flask(__name__)

conn = psycopg2.connect(URL['DB'], sslmode='require')
conn.autocommit = True
cur = conn.cursor()

from app import tgbot
