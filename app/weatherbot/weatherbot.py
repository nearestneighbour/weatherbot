from app import cur, URL, sql
from app.weatherbot.weather import get_stats, get_map # change this
from app.weatherbot import URL as wURL

import requests
from PIL import Image
from io import BytesIO

def process_msg(chat_id, msg):
    if 'location' in msg:
        set_location(chat_id, coord=msg['location'])
    elif 'text' in msg:
        text = msg['text'].lower().split(' ')
        if text[0] == 'help':
            send_msg(chat_id, help(text))
        elif text[0] == 'location':
            if len(text) == 1:
                get_location(chat_id)
            else:
                set_location(chat_id, loc=' '.join(text[1:]))
        elif text[0] == 'coordinates':
            if len(text) == 1:
                get_location(chat_id)
            else:
                set_location(chat_id, coord=text[1])
        elif text[0] == 'stat':
            send_stats(chat_id)
        elif text[0] == 'map':
            send_map(chat_id, text)

def send_stats(chat_id):
    coord = get_location(chat_id, False)
    if coord == None:
        send_msg(chat_id, 'Please set location first.')
        return
    coord = [float(i) for i in coord[0].split(',')]
    send_msg(chat_id, get_stats(coord))

def send_map(chat_id, text):
    # best coords: zoom=7, x=65-66, y=41-42 - temp coord: 7/65/42 = or 5/16/10
    coord = get_location(chat_id, False)
    if coord == None:
        send_msg(chat_id, 'Please set location first.')
    else:
        coord = [float(i) for i in coord[0].split(',')]
        send_img(chat_id, get_map(text[1], coord, z=10))

def set_location(chat_id, loc=None, coord=None, send=True):
    if coord == None:
        p = {'q': loc}
    else:
        if isinstance(coord, dict):
            coord = [coord['latitude'],coord['longitude']]
        elif isinstance(coord, str):
            coord = [float(i) for i in coord.split(',')]
        p = {'lat': coord[0], 'lon': coord[1]}
    data = requests.get(wURL['STAT'], params=p).json()
    if ('name' not in data) and send:
        send_msg(chat_id, 'Unknown location.')
    else:
        coord = str(data['coord']['lat']) + ',' + str(data['coord']['lon'])
        loc = data['name'] + ',' + data['sys']['country']
        sql.set(chat_id, coord, loc)
        if send:
            send_msg(chat_id, locationset.format(loc, coord))

def get_location(chat_id, send=True):
    result = sql.find(chat_id)
    if send:
        if result == None:
            send_msg(chat_id, 'Please set location first.')
        else:
            send_msg(chat_id, locationset.format(result[1], result[0]))
    return result

def help(text):
    #if len(text) == 1:
    #    return mainhelp
    return ''

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



mainhelp = """Hi there. Here's how to use the weatherbot:
Example commands:
**location <location>** sets the current location to a city/region/...
**coordinates 51.84,8.84** sets the current location to lat 51.84, lon 8.84
**map wind** gives a wind map over your current location. Other maps are *clouds,
\bprecipitation, temp, pressure, sat*
**stat** gives some weather statistics

Type 'help command' to get more info on a specific command.
\bType 'help' to see this help message."""

locationset = """Location: {}\nCoordinates: {}
Wrong country? Try specifying country code after city, e.g. ''location Nijmegen,NL''"""
