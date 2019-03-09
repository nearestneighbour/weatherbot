import requests
from io import BytesIO

from app import URL

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
