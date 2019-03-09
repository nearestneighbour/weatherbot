import requests
from io import BytesIO
from PIL import Image

from app import app, db, URL

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return 'no data'
    if 'message' in data:
        chat = data['message']['chat']['id']

        # Check for system command (e.g. change bot)
        if 'text' in data['message']:
            txt = data['message']['text'].lower()
            if txt[0] == '/' and len(txt) > 1: # change bot
                bot = getmodule(txt=txt[1:])
                if bot == None:
                    send_msg(chat, 'Couldn''t change bot.')
                else:
                    db.set('state', chat, txt[1:])
                    send_msg('Changed bot to: ' + txt[1:]))
                return ''

        # Check for bot command
        bot = getmodule(chat_id=chat)
        if bot == None:
            send_msg('Set bot first with command /bot.')
        else:
            bot.process_msg(chat, data['message'])

    return ''

def getmodule(chat_id=None, txt=None):
    if txt == None:
        txt = db.get('state', chat_id)
    if txt in BOTS:
        return BOTS[txt]
    return None

def send_msg(chat_id, text):
    data = {'chat_id':chat_id, 'text':text, 'parse_mode':'Markdown'}
    requests.post(URL['BOT'] + 'sendMessage', json=data)

def send_img(chat_id, img):
    if isinstance(img, object):
        bio = BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0) # remove?
        f = {'photo': ('1.png',bio,'image/png')}
        requests.post(URL['BOT'] + 'sendPhoto?chat_id=' + str(chat_id), files=f)
