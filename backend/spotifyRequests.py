#This is a file for retrieving data from Spotify. It's pretty hype.

import requests
import json
import ast
import numpy as np
from requests_toolbelt.utils import dump
from database import *
from relDatabase import *

#builds authorization header for API requests
def buildAuthHeader(token):
    return {'Authorization' : "Bearer " + token}

#gets a user's id
def getUserID(token):
    authHeader = buildAuthHeader(token)
    userData = json.loads(requests.get("https://api.spotify.com/v1/me", headers = authHeader).text)
    return userData['id']

#gets a user's id
def getUsername(token):
    authHeader = buildAuthHeader(token)
    userResponse = requests.get("https://api.spotify.com/v1/me", headers = authHeader).text
    userData = json.loads(userResponse)
    return userData['display_name']

#insert user to database
def insertUser(token):
    authHeader = buildAuthHeader(token)
    userResponse = requests.get("https://api.spotify.com/v1/me", headers = authHeader).text
    userData = json.loads(userResponse)
    insert_user(userData['id'], userData['display_name'])
    print(userData['id'] + userData['display_name'])
    return userData['display_name'], userData['id']

#get show
def getShow(token, showID):
    authHeader = buildAuthHeader(token)
    showResponse = requests.get('https://api.spotify.com/v1/shows/' + showID, headers = authHeader)
    show = json.loads(showResponse.text)
    return show

#get multiple shows
def getShows(token, showIDs):
    authHeader = buildAuthHeader(token)
    showResponse = requests.get('https://api.spotify.com/v1/shows', headers = authHeader, params = {'ids' : ",".join(showIDs)})
    shows = json.loads(showResponse.text)['shows']
    return shows

#adds the user's most recently played song, but holds the ability to send more than one if we choose to implement that in the SQL file
def addRecentlyListened(token, limit=1):
    authHeader = buildAuthHeader(token)
    data = json.loads(requests.get('https://api.spotify.com/v1/me/player/recently-played', headers = authHeader, params = {'limit' : limit}).text)
    for item in data['items']:
        track = item['track']
        featureData = json.loads(requests.get('https://api.spotify.com/v1/audio-features/' + track['id'], headers = authHeader, params = {'id' : track['id']}).text)
        insert_recently_played(getUserID(token), track['id'], track['name'], featureData['acousticness'], featureData['danceability'], featureData['energy'],
                                featureData['instrumentalness'], featureData['liveness'], featureData['speechiness'], featureData['valence'], featureData['tempo'],
                                "noGenre")


#Deletes the user's recently played song in the database
def deleteUserRecentlyPlayed(token):
    authHeader = buildAuthHeader(token)
    userID = getUserID(token)
    delete_recently_played(userID)
    deleteUser(userID)

#Returns the user's most recently played song in the database
def getRecentlyListened(token):
    userID = getUserID(token)
    tableEntry = retrieve_recently_played(userID)
    if tableEntry:
        return tableEntry[2]
    return "Empty"
    
#function to insert the top songs of a user to the relational database. Default limit is 50
def getTopTracks(token, limit = 100):
    authHeader = buildAuthHeader(token)
    topTracks = json.loads(requests.get('https://api.spotify.com/v1/me/top/tracks', headers = authHeader, params = {'limit' : limit}).text)
    trackList = []
    genres = []
    userID = getUserID(token)
    for item in topTracks['items']:
        track = item
        featureData = json.loads(requests.get('https://api.spotify.com/v1/audio-features/' + track['id'], headers = authHeader, params = {'id' : track['id']}).text)
        artistUrl = 'https://api.spotify.com/v1/artists/' + track['artists'][0]['id']
        artistData = json.loads(requests.get(artistUrl, headers = authHeader).text)
        # print(artistData)
        genre = ""
        if (len(artistData['genres']) != 0):
            genre = artistData['genres'][0]
            for g in artistData['genres']:
                genres.append(g)
        # print(track['uri'])
        trackList.append([track['id'], track['name'], track['uri'], featureData['acousticness'], featureData['danceability'], featureData['energy'],
                                featureData['instrumentalness'], featureData['liveness'], featureData['speechiness'], featureData['valence'], featureData['tempo'],
                                genre, artistData['id'], artistData['name']])
    insert_user_favorite_songs(userID, getUsername(token), trackList)
    insertGenres(userID, genres)


#function to get top artists of a user. Default limit is 50
def getTopArtists(token, limit = 50):
    authHeader = buildAuthHeader(token)
    topArtists = json.loads(requests.get('https://api.spotify.com/v1/me/top/artists', headers = authHeader, params = {'limit' : limit}).text)

#function to get all user's saved tracks
def getUserLibrary(token):
    authHeader = buildAuthHeader(token)
    url = 'https://api.spotify.com/v1/me/tracks'
    libraryData = json.loads(requests.get(url, headers = authHeader).text)

#function to insert into relational database all user's saved shows
def insertUserShows(token):
    authHeader = buildAuthHeader(token)
    url = 'https://api.spotify.com/v1/me/shows'
    showData = json.loads(requests.get(url, headers = authHeader).text)
    print("request finished")
    showsRel = []
    showsNeo = []
    for item in showData['items']:
        show = item['show']
        showsRel.append((show['id'], show['name']))
        showsNeo.append(show['id'])
    print("for loop finished")
    userID = getUserID(token)
    insert_show(showsRel)
    insertShows(userID, showsNeo)
    


#helper function to get the follower data for a user
def checkFollowing(token):
    userID = getUserID(token)
    userIDs = retrieve_active_userIDs()
    string = ","
    userIDList = string.join(userIDs)
    authHeader = buildAuthHeader(token)
    userUrl = 'https://api.spotify.com/v1/me/following/contains'
    userFollowData = requests.get(userUrl, headers = authHeader, params = {'ids' : userIDList, 'type' : 'user'}).text
    followholder = userFollowData[2:len(userFollowData)-2]
    splitt = followholder.split(', ')
    artistUrl = 'https://api.spotify.com/v1/me/following?type=artist'
    artistFollowData = json.loads(requests.get(artistUrl, headers = authHeader).text)
    artistFollowList = []
    for artist in artistFollowData['artists']['items']:
        artistFollowList.append(artist['id'])
    return userID, userIDs, artistFollowList, userIDList, splitt

#function to update neo4j with follow data upon login
def updateFollows(token):
    userID, userIDs, artistIDList, userIDList, userFollowData = checkFollowing(token)
    for idx in range(len(artistIDList)):
        if artistIDList[idx]:
            createListen(userID, artistIDList[idx])
    for idx in range(len(userIDs)):
        if userFollowData[idx] == 'true':
            createFriendship(userID, userIDs[idx])

# function to determine which shows a user might like
def findRecommendedShows(userID, number=3):
    shows = retrieve_show_ids()
    usersShows = findShows(userID)
    print(usersShows)
    following = findFriends(userID)
    showList = {}
    for show in shows:
        if show in usersShows:
            continue
        showListeners = findShowListeners(show)
        followedListeners = 0
        for f in following:
            if f in showListeners:
                followedListeners += 1
        followpct = followedListeners / len(following)

        showGenres = findShowLikes(show)
        userGenres = findLikes(userID)

        similarity = 1
        for genre in userGenres:
            if genre not in showGenres:
                similarity -= userGenres[genre]
            else:
                similarity -= abs(userGenres[genre] - showGenres[genre])
        showList[show] = similarity + followpct
    sortedShows = dict(sorted(showList.items(), key=lambda item:item[1]))
    if (number <= len(sortedShows.keys())):
        return list(sortedShows.keys())[0:number]
    else:
        return list(sortedShows.keys())

#function to have user save a show
def saveShow(token, showID):
    authHeader = buildAuthHeader(token)
    requests.put('https://api.spotify.com/v1/me/shows', headers = authHeader, params = {'ids' : showID})

#function to make the playlist in spotify
def createPlaylist(token, userID, songURIs, name):
    authHeader = {'Authorization' : "Bearer " + token}
    createResponse = requests.post('https://api.spotify.com/v1/users/' + userID + '/playlists', headers = authHeader, json ={'name' : name})
    playlistID = json.loads(createResponse.text)['id']
    addedResponse = requests.post('https://api.spotify.com/v1/playlists/' + playlistID + '/tracks', headers = authHeader, params = {'uris' : ",".join(songURIs)})


#build playlist
def buildPlaylistAllFollowing(token):
    userID = getUserID(token)
    friends = findFriends(userID)
    preferences = []
    for friend in friends:
        preferences.append(getAveragePrefs(friend))
    matrix = np.array(preferences)
    averages = np.mean(matrix, axis=0)
    playlist = makePlaylistGivenAvg(np.ndarray.tolist(averages))
    return playlist

#get a dictionary relating friend id to friend name for friends
def getFollowingUsers(userID):
    friends = findFriends(userID)
    users = retrieve_active_userNameID()
    ret = {}
    for friend in friends:
        ret[friend] = users[friend]
    return ret

def buildPlaylistFromFriendData(userID, friendID):
    preferences = []
    preferences.append(getAveragePrefs(friendID))
    preferences.append(getAveragePrefs(userID))
    matrix = np.array(preferences)
    averages = np.mean(matrix, axis=0)
    playlist = makePlaylistGivenAvg(np.ndarray.tolist(averages))
    return playlist

def syncUserData(token):
    getTopTracks(token)
    print("top tracks inserted")
    insertUserShows(token)

def addPlaylist(token, uriList, name):
    userID = getUserID(token)
    createPlaylist(token, userID, uriList, name)
    return "yup"

def getShowNames(showList):
    shows = retrieve_shows()
    ret = []
    for showID in showList:
        ret.append(shows[showID])
    return ret