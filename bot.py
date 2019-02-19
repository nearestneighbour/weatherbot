from flask import Flask, request
import requests

app = Flask(__name__)
BOT_URL = 'https://api.telegram.org/bot694985196:AAFoZWhhsDF4qyvj0bJQNjn89PZypztg3Xc/'

def send_message(prepared_data):
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)

@app.route('/hello')
def hello_world():
    return 'Hello, World!12'

@app.route('/', methods='GET')
def getmsg():
    chid = request.form['chat_id']
    msg = request.form['text']
    send_message({'chat_id':chid,'text':msg})
