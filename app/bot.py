from app import app, URL, sql

import requests
import os
from math import tan, cos, pi, floor
from PIL import Image
from io import BytesIO

class tgbot:
    def __init__(self, chat_id, msg, cur, coord=None):
        self.chat_id = chat_id
        self.cur = cur # SQL DB cursor
        self.location = None
        self.coord = None
        self.set_location(coord=coord, send=False)
        self.process_msg(msg)

    def process_msg(self, msg):
        if 'location' in msg:
            self.set_location(coord=msg['location'])
        elif 'text' in msg:
            txt = msg['text'].lower().split(' ')
            if txt[0] == 'help':
                self.send_msg(self.help(txt))
            elif txt[0] == 'location':
                self.set_location(loc=' '.join(txt[1:]))
            elif txt[0] == 'coordinates':
                self.set_location(coord=txt[1])
            elif txt[0] == 'stat':
                self.send_stats()
            elif txt[0] == 'map':
                self.send_map(txt)

    def set_location(self, loc=None, coord=None, send=True):
        if coord == None:
            if loc == None:
                return
            else:
                self.location = loc
                p = {'q':loc}
        elif isinstance(coord, dict):
            self.coord = [coord['latitude'],coord['longitude']]
            p = {'lat':coord['latitude'], 'lon':coord['longitude']}
        elif isinstance(coord, str):
            self.coord = [float(i) for i in coord.split(',')]
            p = {'lat':self.coord[0], 'lon':self.coord[1]}
        data = requests.get(URL['STAT'], params=p).json()
        if 'name' not in data and send:
            self.send_msg('Unknown location.')
            return
        self.location = data['name'] + ',' + data['sys']['country']
        self.coord = [data['coord']['lat'],data['coord']['lon']]
        if send:
            self.send_msg(locationset.format(self.location,self.coord))
        self.cur.execute(sql.set(self.chat_id, '{},{}'.format(self.coord[0],self.coord[1])))

    def send_stats(self):
        if self.location == None:
            self.send_msg('Please set location first.')
            return
        p = {'lat':self.coord[0], 'lon':self.coord[1]}
        data = requests.get(URL['STAT'], params=p).json()
        weather = {'Weather':data['weather'][0]['description']}
        weather['Temperature'] = ftoc(data['main']['temp'])
        weather['Humidity'] = data['main']['humidity']
        txt = ''
        for k, v in weather.items():
            txt += '{}: {}\n'.format(k,v)
        self.send_msg(txt[:-1])

    def send_map(self, txt):
        # best coords: zoom=7, x=65-66, y=41-42 - temp coord: 7/65/42 = or 5/16/10
        if self.location == None:
            self.send_msg('Please set location first.')
            return
        z, x, y = 7, 65, 42
        #x, y = geotocoord(self.coord, z)
        if len(txt) == 1:
            data = requests.get(URL['MAP'].format(z, x, y))
        else:
            data = requests.get(URL['WMAP'].format(txt[1],z,x,y))
        img = Image.open(BytesIO(data.content))
        #img = Image.blend(map_img, temp_img, 0.5)
        bio = BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0) # remove?
        f = {'photo': ('1.png',bio,'image/png')}
        requests.post(URL['BOT'] + 'sendPhoto?chat_id=' + str(self.chat_id), files=f)

    def help(self, txt):
        #if len(txt) == 1:
        #    return mainhelp
        return ''

    def send_msg(self, text):
        data = {'chat_id':self.chat_id, 'text':text}
        requests.post(URL['BOT'] + 'sendMessage', json=data)

    def send_img(self, img):
        pass

def ftoc(f): # fahrenheit to celcius
    c = (f-32)*5/9
    return floor(10*c)/10

def geotocoord(coord, zoom):
    n = 2**zoom
    x = n * (coord[1]+180) / 360 # lon
    lat = pi * coord[0] / 180
    y = n * (1 - (log(tan(lat) + 1/cos(lat)) / pi)) / 2
    return x, y


mainhelp = """Hi there. Here's how to use the weatherbot:
command [options]
Commands: map, stat, location, coord
Examples of commands:
'location Nijmegen' sets the current location to Nijmegen.
'coordinates 51.84,8.84' sets the current location to lat.51.84, lon.8.84
'stat temp' gives the current temperature on the current location.
'map clouds Tilburg' gives a map with clouding above the current location.
Type 'help command' to get more info on a specific command.
\bType 'help' to see this help message."""

locationset = """Location: {}\nCoordinates: {}
Wrong country? Try specifying country code after city, e.g. ''location Nijmegen,NL''"""
