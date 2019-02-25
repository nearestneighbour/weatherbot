from app import app, bot

from flask import request

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return 'no data'
    if 'message' in data:
        msg = data['message']
        chat_id = msg['chat']['id']
        bot.process_msg(chat_id, msg)
    return ''
