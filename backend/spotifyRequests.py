#This is a file for retrieving data from Spotify. It's pretty hype.

import requests
import json

def addRecentlyListened(token):
    authHeader = {'Authorization' : "Bearer " + token}
    params = {'limit' : 1}
    results = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers = authHeader, params = params)
    data = json.loads(results.text)
    print(data['items'][0]['track']['name'])