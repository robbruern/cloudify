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

#gets a user's id
def getUsername(token):
    authHeader = {'Authorization' : "Bearer " + token}
    userResults = requests.get("https://api.spotify.com/v1/me", headers = authHeader)
    userData = json.loads(userResults.text)
    return userData['display_name']


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

# TO DO: Add a method that adds the top 50 songs of a user to sql database
# we can add more or less, but 50 seems like the limit of this method
# https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/
# Also as a sidenote, even if we delete users I think we should delete songs
# from UsersFavoriteSongs, but not SpotifySong table

    
#function to get top songs of a user. Default limit is 50
def getTopTracks(token, limit = 50):
    authHeader = {'Authorization' : "Bearer " + token}
    topTracks = json.loads(requests.get('https://api.spotify.com/v1/me/top/tracks', headers = authHeader, params = {'limit' : limit}))

#function to get top artists of a user. Default limit is 50
def getTopArtists(token, limit = 50):
    authHeader = {'Authorization' : "Bearer " + token}
    topArtists = json.loads(requests.get('https://api.spotify.com/v1/me/top/artists', headers = authHeader, params = {'limit' : limit}))

#function to get all user's saved tracks
def getUserLibrary(token):
    authHeader = {'Authorization' : "Bearer " + token}
    url = 'https://api.spotify.com/v1/me/tracks'
    libraryData = json.loads(requests.get(url, headers = authHeader))

#function ot get all user's saved podcasts (shows)
def getUserPodcasts(token):
    authHeader = {'Authorization' : "Bearer " + token}
    url = 'https://api.spotify.com/v1/me/shows'
    showData = json.loads(requests.get(url, headers = authHeader))


#function to determine if a user follows another user
def checkFollowing(token, IDList):
    #TODO: get list of users and artists from neo4j or relational database
    userIDs = retrieve_active_userIDs()
    artistIDs = retrieve_artistIDs()
    string = ", "
    userIDList = string.join(userIDs)
    artistIDList = string.join(artistIDs)
    print(userIDList)
    print(artistIDList)
    authHeader = {'Authorization' : "Bearer " + token}
    url = 'https://api.spotify.com/v1/me/following/contains'
    userFollowData = json.loads(requests.get(url, headers = authHeader, params = {'ids' : userIDList}))
    artistFollowData = json.loads(requests.get(url, headers = authHeader, params = {'ids' : artistIDList}))
    