from flask import request
import requests

from app import app, db, URL, BOTS
from app.chatfunc import send_msg

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return 'no data'
    if 'message' in data:
        chat_id = data['message']['chat']['id']

        # Check for system command (e.g. change bot)
        if 'text' in data['message']:
            txt = data['message']['text'].lower()
            if txt[0] == '/' and len(txt) > 1: # change bot
                bot = getmodule(txt=txt[1:])
                if bot == None:
                    send_msg(chat_id, 'Couldn''t change bot.')
                else:
                    db.set('state', chat_id, txt[1:])
                    send_msg(chat_id, 'Changed bot to: ' + txt[1:])
                return ''

        # Check for bot command
        bot = getmodule(chat_id=chat_id)
        if bot == None:
            send_msg(chat_id, 'Set bot first with command /[bot].')
        else:
            bot.process_msg(chat_id, data['message'])

    return ''

def getmodule(chat_id=None, txt=None):
    if txt == None:
        txt = db.get('state', chat_id)
    if txt in BOTS:
        return BOTS[txt]
    return None
