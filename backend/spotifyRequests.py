#This is a file for retrieving data from Spotify. It's pretty hype.

import requests
import json
from database import *

#gets a user's id
def getUserID(token):
    authHeader = {'Authorization' : "Bearer " + token}
    userResults = requests.get("https://api.spotify.com/v1/me", headers = authHeader)
    userData = json.loads(userResults.text)
    return userData['id']


#adds the user's most recently played song, but holds the ability to send more than one if we choose to implement that in the SQL file
def addRecentlyListened(token):
    authHeader = {'Authorization' : "Bearer " + token}
    params = {'limit' : 1}
    recentlyPlayedResults = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers = authHeader, params = params)
    data = json.loads(recentlyPlayedResults.text)
    print(recentlyPlayedResults.text)
    for item in data['items']:
        track = item['track']
        audioFeaturesResults = requests.get('https://api.spotify.com/v1/audio-features/' + track['id'], headers = authHeader, params = {'id' : track['id']})
        featureData = json.loads(audioFeaturesResults.text)
        insert_recently_played(getUserID(token), track['id'], track['name'], featureData['acousticness'], featureData['danceability'], featureData['energy'],
                                featureData['instrumentalness'], featureData['liveness'], featureData['speechiness'], featureData['valence'], featureData['tempo'],
                                "noGenre")
    print(data['items'][0]['track']['name'])


#Deletes the user's recently played song in the database
def deleteUserRecentlyPlayed(token):
    authHeader = {'Authorization' : "Bearer " + token}
    userID = getUserID(token)
    delete_recently_played(userID)

#Returns the user's most recently played song in the database
def getRecentlyListened(token):
    userID = getUserID(token)
    print(retrieve_recently_played(userID))
    tableEntry = retrieve_recently_played(userID)
    if tableEntry:
        return tableEntry[2]
    return "Empty"
    