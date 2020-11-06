#This is a file for retrieving data from Spotify. It's pretty hype.

import requests
import json
from database import *


insert_recently_played(userID, songID, songName, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, genre)

def getUserID(token):
    authHeader = {'Authorization' : "Bearer " + token}
    userResults = requests.get("https://api.spotify.com/v1/me", headers = authHeader)
    userData = json.loads(userResults.text)
    return userData['id']



def addRecentlyListened(token):
    authHeader = {'Authorization' : "Bearer " + token}
    params = {'limit' : 1}
    recentlyPlayedResults = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers = authHeader, params = params)
    data = json.loads(recentlyPlayedResults.text)
    for item in data['items']:
        track = item['track']
        audioFeaturesResults = requests.get('https://api.spotify.com/v1/audio-features/' + track['id'], headers = authHeader, params = {'id' : trackID})
        featureData = json.loads(audioFeaturesResults.text)
        insert_recently_played(getUserID(token), track['id'], track['name'], featureData['acousticness'], featureData['danceability'], featureData['energy'],
                                featureData['instrumentalness'], featureData['liveness'], featureData['speechiness'], featureData['valence'], featureData['tempo'],
                                featureData['genre'])
    print(data['items'][0]['track']['name'])