from flask import Flask

mychat = 571267260
API_KEY = '694985196:AAFoZWhhsDF4qyvj0bJQNjn89PZypztg3Xc'
BOT_URL = 'https://api.telegram.org/bot' + API_KEY + '/'

app = Flask(__name__)

from app import bot
