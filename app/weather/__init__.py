# should import weather.py
# should declare API/URLs just like ../__init__.py
# declare map names? (and other metadata)

import os

API = {
    'OWM': os.environ['api_owm'],
    'HEREID': os.environ['here_appid'],
    'HEREC': os.environ['here_appc']
}
URL = {
    'STAT': 'http://api.openweathermap.org/data/2.5/weather?appid=' + API['OWM'],
    'MAP':  'https://image.maps.api.here.com/mia/1.6/mapview?app_id={}&app_code={}&nodot'
    .format(API['HEREID'],API['HEREC']),
    'WMAP': 'https://tile.openweathermap.org/map/{}_new/{}/{}/{}.png?appid=' + API['OWM']
    #'SAT':  'http://sat.owm.io/sql/{}/{}/{}?from=cloudless&appid=' + api_owm,
    #'MAP':  'https://a.tile.openstreetmap.org/{}/{}/{}.png'
}

# sat map:
# https://image.maps.api.here.com/mia/1.6/mapview?c=51.8412%2C5.8159&t=1&vt=0&z=9&app_id=SizRSPtIbyRjBjcn1oX3&app_code=eD5qwyNJwBBcK6jEG0lVXQ&w=256&h=256

from app.weather.weather import process_msg
