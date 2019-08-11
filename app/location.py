import requests

from . import HERE_APP_ID, HERE_APP_CODE

auth = 'app_id={}&app_code={}'.format(HERE_APP_ID, HERE_APP_CODE)
loc_url = 'https://geocoder.api.here.com/6.2/geocode.json?' + auth
coord_url = 'https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?' + auth

class location:
    def __init__(self, **kwargs):
        loc = kwargs.pop('loc', None)
        coord = kwargs.pop('coord', None)
        self.set(loc=loc, coord=coord)

    def set(self, loc=None, coord=None):
        if coord:
            self.coord = format_coord(coord)
            self.loc = loc_from_coord(coord)
        elif loc:
            self.loc = loc
            self.coord = coord_from_loc(loc)

    def valid(self):
        return (self.coord != None and self.loc != None)

    def entry(self):
        coord = ','.join(self.coord)
        return '_'.join([coord, self.loc])

    def text(self):
        if self.valid():
            coord = ','.join(self.coord)
            return 'Location: {}\nCoordinates: {}'.format(self.loc, coord)
        else:
            return "Location invalid"

    @staticmethod
    def from_str(string):
        coord, loc = string.split('_')
        coord = format_coord(coord)
        return location(loc=loc, coord=coord)

def loc_from_coord(coord):
    coord = ','.join(format_coord(coord))
    p = {'prox': coord, 'mode': 'retrieveAreas'}
    data = requests.get(coord_url, params=p).json()['Response']['View']
    if len(data) == 0:
        return None
    return data[0]['Result'][0]['Location']['Address']['City']

def coord_from_loc(loc):
    p = {'searchtext': loc}
    data = requests.get(loc_url, params=p).json()['Response']['View']
    if len(data) == 0:
        return None
    coord = data[0]['Result'][0]['Location']['DisplayPosition']
    return format_coord(coord)

def format_coord(coord):
    if isinstance(coord, dict):
        if 'Latitude' in coord:
            coord = [str(coord['Latitude']), str(coord['Longitude'])]
        else:
            coord = [str(coord['latitude']), str(coord['longitude'])]
    elif isinstance(coord, str):
        coord = [i for i in coord.split(',')]
    elif isinstance(coord, list):
        coord = [str(i) for i in coord]
    return coord
