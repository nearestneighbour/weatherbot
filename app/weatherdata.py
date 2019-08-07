import requests
from math import log, tan, cos, pi, floor
from PIL import Image
from io import BytesIO

from . import API_OWM

url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + API_OWM

def get_stats(coord):
    p = {'lat': coord[0], 'lon': coord[1]}
    data = requests.get(url, params=p).json()
    w = {'Weather': data['weather'][0]['description']}
    w['Temperature'] = floor(10*data['main']['temp'] - 2731.5) / 10 # K to C
    w['Humidity'] = data['main']['humidity']
    text = ''
    for k, v in w.items():
        text += '{}: {}\n'.format(k,v)
    return text[:-1]

########## outdated

#'MAP':  'https://image.maps.api.here.com/mia/1.6/mapview?app_id={}&app_code={}&nodot'
#        .format(API['HEREID'],API['HEREC']),
#'WMAP': 'https://tile.openweathermap.org/map/{}_new/{}/{}/{}.png?appid=' + API['OWM']
#'SAT':  'http://sat.owm.io/sql/{}/{}/{}?from=cloudless&appid=' + api_owm,
#'MAP':  'https://a.tile.openstreetmap.org/{}/{}/{}.png'

def get_map(map, coord, z):
    if map == 'pic':
        p = {'lat': coord[0], 'lon': coord[1], 'vt': 1, 't': 2, 'z': z}
        data = requests.get(URL['MAP'], params=p)
        return Image.open(BytesIO(data.content))
    elif map == 'sat':
        p = {'lat': coord[0], 'lon': coord[1], 'vt': 1, 't': 1, 'z': z}
        data = requests.get(URL['MAP'], params=p)
        return Image.open(BytesIO(data.content))
    else:
        return get_weathermap(map, coord, z)

def get_weathermap(map, coord, z):
    x, y = geotocoord(coord, z)
    x, y = floor(x), floor(y)
    data = requests.get(URL['WMAP'].format(map,z,x,y))
    # center picture
    return Image.open(BytesIO(data.content))

def geotocoord(coord, zoom):
    n = 2**zoom
    x = n * (coord[1]+180) / 360 # lon
    lat = pi * coord[0] / 180
    y = n * (1 - (log(tan(lat) + 1/cos(lat)) / pi)) / 2
    return x, y
