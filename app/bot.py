from app import app, URL, sql

import requests
import os
from math import tan, cos, pi
from PIL import Image
from io import BytesIO

class tgbot:
    def __init__(self, chat_id, msg, cur, coord=None):
        self.chat_id = chat_id
        self.cur = cur # SQL DB cursor
        self.location = None
        if coord != None:
            self.coord = coord.split(',')
            self.set_location(self.coord, False)
        else:
            self.coord = coord
        self.process_msg(msg)

    def process_msg(self, msg):
        if 'location' in msg:
            self.set_location(msg['location'])
        elif 'text' in msg:
            txt = msg['text'].lower().split(' ')
            if txt[0] == 'help':
                self.send_msg(self.help(txt))
            elif txt[0] == 'location':
                self.set_location(' '.join(txt[1:]))
            elif txt[0] == 'coordinates':
                self.set_location(txt[1].split(','))
            elif txt[0] == 'stat':
                self.send_stats()
            elif txt[0] == 'map':
                self.send_map(txt)

    def set_location(self, loc, send=True):
        p = {}
        if isinstance(loc, dict):
            self.coord = [loc['latitude'],loc['longitude']]
            p = {'lat':loc['latitude'], 'lon':loc['longitude']}
        elif isinstance(loc, list):
            self.coord = [float(i) for i in loc]
            p = {'lat':loc[0], 'lon':loc[1]}
        elif isinstance(loc, str):
            self.location = loc
            p = {'q':loc}
        data = requests.get(URL['STAT'], params=p).json()
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
            txt += '{:11}: {:.2f}\n'.format(k,v)
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
    return (f-32)*5/9

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
