import requests
from io import BytesIO

from . import API_TG

url = 'https://api.telegram.org/bot' + API_TG + '/'

def send_msg(chat_id, text):
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    requests.post(url + 'sendMessage', json=data)

def send_img(chat_id, img):
    if isinstance(img, object):
        bio = BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0) # remove?
        f = {'photo': ('1.png',bio,'image/png')}
        requests.post(url + 'sendPhoto?chat_id=' + str(chat_id), files=f)
