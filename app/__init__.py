from flask import Flask
import os, sys

app = Flask(__name__)

API = {'TG': os.environ['api_tg']}
URL = {
    'DB':   os.environ['DATABASE_URL'],
    'BOT':  'https://api.telegram.org/bot' + API['TG'] + '/'
}

from app import sql
db = sql.sql(URL['DB'])

from app import weather#, wallet, wiki
BOTS = {
    'weather': sys.modules['weather']
}

from app import tgbot
