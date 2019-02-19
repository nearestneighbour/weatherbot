import requests

text = 'Temperatuur: {} C\nWind: {} m/s\nRegenkans: {}%'
url = 'https://weerlive.nl/api/json-10min.php?locatie='

def getweather(loc):
    if isinstance(loc, dict):
        loc = str(loc['latitude']) + ',' + str(loc['longitude'])

    data = requests.get(url + loc, timeout=10).json()
    data = data['liveweer'][0]
    
    response = text.format(data['temp'],data['windms'],data['d0neerslag'])
    return response
