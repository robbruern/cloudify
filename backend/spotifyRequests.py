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

def addUserLibraryToDatabase(token):
    authHeader = {'Authorization' : "Bearer " + token}
    userID = getUserID(token)
    libraryData = json.loads(requests.get('https://api.spotify.com/v1/me/tracks', header = authHeader, params = {'limit' : 50}).text)
    for item in libraryData['item']:
        track = item['track']
        audioFeaturesResults = requests.get('https://api.spotify.com/v1/audio-features/' + track['id'], headers = authHeader, params = {'id' : track['id']})
        featureData = json.loads(audioFeaturesResults.text)
        # insert_favorites(getUserID(token), track['id'], track['name'], featureData['acousticness'], featureData['danceability'], featureData['energy'],
        #                         featureData['instrumentalness'], featureData['liveness'], featureData['speechiness'], featureData['valence'], featureData['tempo'],
        #                         "noGenre")
        

# TO DO: Add a method that adds the top 50 songs of a user to sql database
# we can add more or less, but 50 seems like the limit of this method
# https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/
# Also as a sidenote, even if we delete users I think we should delete songs
# from UsersFavoriteSongs, but not SpotifySong table

    
