#This is a file for retrieving data from Spotify. It's pretty hype.

import requests
import json
import ast
from requests_toolbelt.utils import dump
from database import *
from relDatabase import *

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
    # print(data['items'][0]['track']['name'])


#Deletes the user's recently played song in the database
def deleteUserRecentlyPlayed(token):
    authHeader = {'Authorization' : "Bearer " + token}
    userID = getUserID(token)
    delete_recently_played(userID)

#Returns the user's most recently played song in the database
def getRecentlyListened(token):
    userID = getUserID(token)
    # print(retrieve_recently_played(userID))
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
    req = requests.get('https://api.spotify.com/v1/me/top/tracks', headers = authHeader, params = {'limit' : limit})
    # data = dump.dump_all(req)
    # print("REQUEST RETURNED: " + data.decode('utf-8'))
    # print("REQUEST RETURNED: " + req.text)
    topTracks = json.loads(req.text)
    trackList = []
    userID = getUserID(token)
    for item in topTracks['items']:
        # print("THE ITEM IS-------------------------" + str(item))
        track = item
        audioFeaturesResults = requests.get('https://api.spotify.com/v1/audio-features/' + track['id'], headers = authHeader, params = {'id' : track['id']})
        featureData = json.loads(audioFeaturesResults.text)

        artistUrl = 'https://api.spotify.com/v1/artists/' + track['artists'][0]['id']
        artistData = json.loads(requests.get(artistUrl, headers = authHeader).text)
        genre = ""
        if (len(artistData['genres']) != 0):
            genre = artistData['genres'][0]
        trackList.append([track['id'], track['name'], featureData['acousticness'], featureData['danceability'], featureData['energy'],
                                featureData['instrumentalness'], featureData['liveness'], featureData['speechiness'], featureData['valence'], featureData['tempo'],
                                genre, artistData['id'], artistData['name']])
    insert_user_favorite_songs(userID, getUsername(token), trackList)


#function to get top artists of a user. Default limit is 50
def getTopArtists(token, limit = 50):
    authHeader = {'Authorization' : "Bearer " + token}
    topArtists = json.loads(requests.get('https://api.spotify.com/v1/me/top/artists', headers = authHeader, params = {'limit' : limit}).text)

#function to get all user's saved tracks
def getUserLibrary(token):
    authHeader = {'Authorization' : "Bearer " + token}
    url = 'https://api.spotify.com/v1/me/tracks'
    libraryData = json.loads(requests.get(url, headers = authHeader).text)

#function ot get all user's saved podcasts (shows)
def getUserPodcasts(token):
    authHeader = {'Authorization' : "Bearer " + token}
    url = 'https://api.spotify.com/v1/me/shows'
    showData = json.loads(requests.get(url, headers = authHeader).text)


#function to determine if a user follows another user
def checkFollowing(token):
    #TODO: get list of users and artists from neo4j or relational database
    userIDs = retrieve_active_userIDs()
    string = ","
    userIDList = string.join(userIDs)
    userID = getUserID(token)
    authHeader = {'Authorization' : "Bearer " + token}
    userUrl = 'https://api.spotify.com/v1/me/following/contains'
    userFollowData = requests.get(userUrl, headers = authHeader, params = {'ids' : userIDList, 'type' : 'user'}).text
    followholder = userFollowData[2:len(userFollowData)-2]
    splitt = followholder.split(', ')
    # print(splitt)
    


    artistUrl = 'https://api.spotify.com/v1/me/following?type=artist'
    artistFollowData = json.loads(requests.get(artistUrl, headers = authHeader).text)
    # print(artistFollowData)
    artistFollowList = []
    for artist in artistFollowData['artists']['items']:
        artistFollowList.append(artist['id'])

    # print(userIDList)
    # print(userFollowData)
    return userID, userIDs, artistFollowList, userIDList, splitt

def updateFollows(token):
    userID, userIDs, artistIDList, userIDList, userFollowData = checkFollowing(token)
    for idx in range(len(artistIDList)):
        if artistIDList[idx]:
            print('artist')
            createListen(userID, artistIDList[idx])
    for idx in range(len(userIDs)):
        if userFollowData[idx] == 'true':
            createFriendship(userID, userIDs[idx])
