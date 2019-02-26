from app import app, weatherbot

from flask import request

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return 'no data'
    if 'message' in data:
        msg = data['message']
        chat_id = msg['chat']['id']
        weatherbot.process_msg(chat_id, msg)
    return ''
