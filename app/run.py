from app import app, cur, sql
from app.bot import tgbot

from flask import request, render_template
import requests

botlist = {}

@app.route('/tgbot', methods=['POST'])
def getmsg():
    data = request.get_json()
    if data == None:
        return ''
    if 'message' in data:
        msg = data['message']
        chat_id = msg['chat']['id']
        if chat_id in botlist:
            botlist[chat_id].process_msg(msg)
        else:
            cur.execute(sql.find(chat_id))
            row = cur.fetchone()
            if row == None:
                cur.execute(sql.new(chat_id))
                botlist[chat_id] = tgbot(chat_id, msg, cur)
            else:
                botlist[chat_id] = tgbot(chat_id, msg, cur, row[1])
    return ''
