#This is a file for retrieving data from Spotify. It's pretty hype.

import requests
import json
import ast
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
    userData = json.loads(requests.get("https://api.spotify.com/v1/me", headers = authHeader).text)
    return userData['display_name']

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

#Returns the user's most recently played song in the database
def getRecentlyListened(token):
    userID = getUserID(token)
    tableEntry = retrieve_recently_played(userID)
    if tableEntry:
        return tableEntry[2]
    return "Empty"
    
#function to get top songs of a user. Default limit is 50
def getTopTracks(token, limit = 50):
    authHeader = buildAuthHeader(token)
    topTracks = json.loads(requests.get('https://api.spotify.com/v1/me/top/tracks', headers = authHeader, params = {'limit' : limit}).text)
    trackList = []
    userID = getUserID(token)
    for item in topTracks['items']:
        track = item
        featureData = json.loads(requests.get('https://api.spotify.com/v1/audio-features/' + track['id'], headers = authHeader, params = {'id' : track['id']}).text)
        artistUrl = 'https://api.spotify.com/v1/artists/' + track['artists'][0]['id']
        artistData = json.loads(requests.get(artistUrl, headers = authHeader).text)
        genre = ""
        if (len(artistData['genres']) != 0):
            genre = artistData['genres'][0]
        trackList.append([track['id'], track['name'], track['uri'], featureData['acousticness'], featureData['danceability'], featureData['energy'],
                                featureData['instrumentalness'], featureData['liveness'], featureData['speechiness'], featureData['valence'], featureData['tempo'],
                                genre, artistData['id'], artistData['name']])
    insert_user_favorite_songs(userID, getUsername(token), trackList)


#function to get top artists of a user. Default limit is 50
def getTopArtists(token, limit = 50):
    authHeader = buildAuthHeader(token)
    topArtists = json.loads(requests.get('https://api.spotify.com/v1/me/top/artists', headers = authHeader, params = {'limit' : limit}).text)

#function to get all user's saved tracks
def getUserLibrary(token):
    authHeader = buildAuthHeader(token)
    url = 'https://api.spotify.com/v1/me/tracks'
    libraryData = json.loads(requests.get(url, headers = authHeader).text)

#function ot get all user's saved podcasts (shows)
def getUserPodcasts(token):
    authHeader = buildAuthHeader(token)
    url = 'https://api.spotify.com/v1/me/shows'
    showData = json.loads(requests.get(url, headers = authHeader).text)


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
            print('artist')
            createListen(userID, artistIDList[idx])
    for idx in range(len(userIDs)):
        if userFollowData[idx] == 'true':
            createFriendship(userID, userIDs[idx])

#function to get a user's saved shows
def getUsersShows(token):
    authHeader = buildAuthHeader(token)
    showsData = json.loads(requests.get('https://api.spotify.com/v1/me/shows', header = authHeader, params = {'limit' : limit}))
    for item in showsData['items']:
        show = item['show']
        showID = show['id']
        showName = show['name']
        #then add show ID and Name to the relational database
        #draw listens to relation to neo4j or add to a table with user and show as the two attributes in the relational database

#function to give a show attributes related to the genres its users listen to
def giveShowAttributes(showID, userID):
    #get artists a user listens to from neo4j
    #iterate over the artists, and increment the genres that the user's top artists are assosciated with
    #add/update the data for a show in the relational database
    return "yup"

#function to determine which shows a user might like
def findRecommendedShows(userID):
    #determine using the percentage of followed users that listen to the podcast and how the podcast aligns with the user's genres to determine if they would like the podcast.
    # for show in shows:
    #     #get number of followed users who also 'watch' said show

    #     #make dictionary storing which percentage of a user's songs fall under each of their followed genres
    #     #make dictionary storing which percentage of a show's listeners songs fall under each of their followed genres
    #     #for the overlapping genres, measure the closeness of the percentages and add up the differences between them
    #     #add to the difference any percentages that a user listens to that aren't part of the podcasts genre list yet.

    #     #Combing the number of followed users who also watch the show and the percentage differences between the overlapping genres.
    #     #sort the shows depending on this number^^^^ to determine the shows a user might like
    return "yup"

#function to have user save a show
def saveShow(token, showID):
    authHeader = buildAuthHeader(token)
    requests.put('https://api.spotify.com/v1/me/shows', headers = authHeader, params = {'ids' : showID})

#function to make the playlist in spotify.
def createPlaylist(token, userID, songURIs, name):
    authHeader = buildAuthHeader(token)
    createResponse = requests.put('https://api.spotify.com/v1/users/' + userID + '/playlists', headers = authHeader, params = {'name' : name})
    playlistID = json.loads(createResponse.text)['id']
    addedResponse = requests.put('https://api.spotify.com/v1/playlists/' + playlistID + '/tracks', headers = authHeader, params = {'uris' : ",".join(songURIs)})
    print(addedResponse.text)



#build playlist
def buildPlaylistAllFollowing():
    #get user breakdown of what their top songs' feature data is
    #go through their friends' top tracks and add that stuff to the breakdown above^
    #average out all the data
    #find songs that match closest all of that data
    return "yup"

def buildPlaylistFromFriendData():
    #use Ricky's playlist making function
    return "yup"

def buildPlaylistOnlyUser():
    #use only the user's data to build a playlist pulling from our song database
    return "yup"

