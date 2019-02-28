from flask import request

from app import app, weather

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return 'no data'
    if 'message' in data:
        msg = data['message']
        chat_id = msg['chat']['id']
        weather.process_msg(chat_id, msg)
    return ''
