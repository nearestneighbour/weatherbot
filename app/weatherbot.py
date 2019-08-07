import requests

from . import DB_URL
from .chat_utils import send_msg
from .location import location
from .sql import sql
from .weatherdata import get_stats

db = sql(DB_URL)

def process_msg( msg):
    chat_id = msg['chat']['id']
    if 'location' in msg:
        set_user_location(chat_id, coord=msg['location'])

    elif 'text' in msg:
        text = msg['text'].lower().split(' ')
        if text[0] == 'location':
            if len(text) == 1:
                loc = get_user_location(chat_id)
                if loc:
                    send_msg(chat_id, loc.text())
                else:
                    send_msg(chat_id, "User location unknown.")
            else:
                set_user_location(chat_id, loc=' '.join(text[1:]))

        elif text[0] == 'weather':
            if len(text) == 1:
                loc = get_user_location(chat_id)
            else:
                loc = location(loc=' '.join(text[1:]))
            send_stats(chat_id, loc)

def send_stats(chat_id, loc):
    if loc.valid():
        coord = [float(i) for i in loc.coord]
        send_msg(chat_id, 'Weather in ' + loc.loc + ':\n' + get_stats(coord))
    else:
        send_msg(chat_id, 'Location invalid')

def set_user_location(chat_id, coord=None, loc=None):
    loc = location(coord=coord, loc=loc)
    if loc.valid():
        db.set('location', chat_id, loc.entry())
    send_msg(chat_id, loc.text())

def get_user_location(chat_id):
    result = db.get('location', chat_id)
    if result:
        return location.from_str(result)

################## outdated

def send_map(chat_id, text):
    # best coords: zoom=7, x=65-66, y=41-42 - temp coord: 7/65/42 = or 5/16/10
    coord = get_location(chat_id, False)
    if coord == None:
        send_msg(chat_id, 'Please set location first.')
    else:
        coord = [float(i) for i in coord[0].split(',')]
        send_img(chat_id, get_map(text[1], coord, z=7))
