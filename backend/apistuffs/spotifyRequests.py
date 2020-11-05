#This is a file for retrieving data from Spotify. It's pretty hype.

import requests
import json

CLIENT_ID = '97f09e12e273458e9cc101218963d6c5'
CLIENT_SECRET = 'd2fbb0f09761413d9130ccb9ac1b4eff'

results = requests.get('https://api.spotify.com/v1/playlists/37i9dQZEVXbLRQDuF5jeBp')
data = json.loads(results.text)
print(data)
for idx, track in enumerate(data['tracks']):
    print(idx, track['track']['name'])