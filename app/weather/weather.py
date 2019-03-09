import requests

from app import db
from app.chatfunc import send_msg, send_img

from app.weather import URL
from app.weather.weatherdata import get_stats, get_map # change this?

def process_msg(chat_id, msg):
    if 'location' in msg:
        set_location(chat_id=chat_id, coord=msg['location'])
    elif 'text' in msg:
        text = msg['text'].lower().split(' ')
        if text[0] == 'help':
            send_msg(chat_id, help(text))
        elif text[0] == 'location':
            if len(text) == 1:
                get_location(chat_id=chat_id)
            else:
                set_location(chat_id=chat_id, loc=' '.join(text[1:]))
        elif text[0] == 'coordinates':
            if len(text) == 1:
                get_location(chat_id=chat_id)
            else:
                set_location(chat_id=chat_id, coord=text[1])
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
        send_img(chat_id, get_map(text[1], coord, z=7))

def set_location(chat_id, coord=None, loc=None, send=True):
    coord, loc = get_location(coord=coord, loc=loc)
    if coord == None or loc == None:
        send_msg(chat_id, 'Unknown location.')
        return
    db.set('location', chat_id, '_'.join([coord,loc]))
    if send:
        send_msg(chat_id, locationset.format(loc, coord))

def get_location(chat_id=None, send=True, coord=None, loc=None):
    if coord == None:
        if loc == None:
            result = db.get('location', chat_id)
            if result != None:
                result = result.split('_')
            if send:
                if result == None:
                    send_msg(chat_id, 'Please set location first.')
                else:
                    send_msg(chat_id, locationset.format(result[1], result[0]))
            return result
        else:
            p = {'q': loc}
    else:
        if isinstance(coord, dict):
            coord = [coord['latitude'],coord['longitude']]
        elif isinstance(coord, str):
            coord = [float(i) for i in coord.split(',')]
        p = {'lat': coord[0], 'lon': coord[1]}
    data = requests.get(URL['STAT'], params=p).json()
    if 'name' not in data:
        return None
    elif coord == None:
        coord = str(data['coord']['lat']) + ',' + str(data['coord']['lon'])
    elif loc == None:
        loc = data['name'] + ',' + data['sys']['country']
    return coord, loc

def help(text):
    #if len(text) == 1:
    #    return mainhelp
    return ''

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
