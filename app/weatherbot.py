import requests
from io import BytesIO

from . import db, TG_URL, OWM_API
from .location import location

def process_msg(msg):
    id = msg['chat']['id']

    if 'location' in msg:
        set_user_location(id, coord=msg['location'])

    elif 'text' in msg:
        text = msg['text'].lower().split(' ')
        if len(text) == 1:
            loc = get_user_location(id)
        else:
            loc = location(loc=' '.join(text[1:]))
        if not (loc and loc.valid()):
            send_msg(id, 'Location unknown.')
            return

        if text[0] == 'location':
            if len(text) == 1:
                send_msg(id, loc.text())
            else:
                set_user_location(id, loc=loc.loc) # yes

        elif text[0] == 'weather':
            send_stats(id, loc)


def send_msg(id, text):
    data = {'chat_id': id, 'text': text, 'parse_mode': 'Markdown'}
    requests.post(TG_URL + '/sendMessage', json=data)

def send_img(id, img):
    if isinstance(img, object):
        bio = BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0) # remove?
        f = {'photo': ('1.png', bio,'image/png')}
        requests.post(TG_URL + '/sendPhoto?chat_id=' + str(id), files=f)

def send_stats(id, loc):
    url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + OWM_API
    p = {'lat': loc.coord[0], 'lon': loc.coord[1]}
    data = requests.get(url, params=p).json()
    w = data['weather'][0]
    m = data['main']
    temps = (m['temp'], m['temp_min'], m['temp_max'])
    temps = ((10*i - 2731.5) // 10 for i in temps) # Kelvin to Celcius

    msgtxt = 'Weather in {}: {}\n'.format(loc.loc, w['description'])
    msgtxt += 'Temperature: {} ({}, {})\n'.format(*temps)
    msgtxt += 'Humidity: {}\nPressure: {}\n'.format(m['humidity'], m['pressure'])
    msgtxt += 'Wind speed: {}'.format(data['wind']['speed'])
    send_msg(id, msgtxt)

def set_user_location(id, coord=None, loc=None):
    loc = location(coord=coord, loc=loc)
    if loc.valid():
        db.set('location', id, loc.entry())
    send_msg(id, loc.text())

def get_user_location(id):
    result = db.get('location', id)
    if result:
        return location.from_str(result)
