import requests
from io import BytesIO

from . import TG_URL

def send_msg(chat_id, text):
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    requests.post(TG_URL + '/sendMessage', json=data)

def send_img(chat_id, img):
    if isinstance(img, object):
        bio = BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0) # remove?
        f = {'photo': ('1.png',bio,'image/png')}
        requests.post(TG_URL + '/sendPhoto?chat_id=' + str(chat_id), files=f)
