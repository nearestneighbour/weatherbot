import requests

# Define API URLs
baseurl = 'https://en.wikipedia.org/w/api.php?redirects&action=query&format=json&utf8='
searchpar = '&list=search&srlimit=1&srprop=&srsearch='
textpar = '&prop=extracts&exlimit=1&exintro=true&explaintext=plain&pageids='

def getwikipage(topic):
    data = requests.get(baseurl + searchpar + topic).json()
    title = data['query']['search'][0]['title']
    pageid = str(data['query']['search'][0]['pageid'])

    url = baseurl + textpar + pageid
    data = requests.get(url).json()
    return data['query']['pages'][pageid]['extract']
