from app import app, db, BOTS
from app.chatfunc import send_msg

def process_msg(msg):
    chat_id = msg['chat']['id']

    if 'text' in msg:
        # Check for system commands (e.g. change bot, help)
        txt = msg['text'].lower()
        if txt[0] == '/':
            if txt == '/bot':
                bot = db.get('state', chat_id)
                if bot == None:
                    send_msg(chat_id, 'No bot chosen.')
                else:
                    send_msg(chat_id, 'Current bot: ' + bot)
            elif txt == '/help':
                pass
            else:
                bot = getmodule(txt=txt[1:])
                if bot == None:
                    send_msg(chat_id, 'Couldn''t change bot.')
                else:
                    db.set('state', chat_id, txt[1:])
                    send_msg(chat_id, 'Changed bot to: ' + txt[1:])
            return

    # Check for bot command
    bot = getmodule(chat_id=chat_id)
    if bot == None:
        send_msg(chat_id, 'Set bot first with command /[bot].')
    else:
        bot.process_msg(chat_id, msg)
    return

def getmodule(chat_id=None, txt=None):
    if txt == None:
        txt = db.get('state', chat_id)
    if txt in BOTS:
        return BOTS[txt]
    return None
