from flask import Flask, request
from flask_cors import CORS, cross_origin
from spotifyRequests import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route('/token', methods = ['POST'])
@cross_origin()
def token():
    tokenData = request.json['token']
    uid = getUserID(tokenData)
    if uid not in retrieve_active_userIDs():
        syncUserData(tokenData)
    userName, userID = insertUser(tokenData)
    updateFollows(tokenData)
    return str(userName) + ',' + str(userID)

@app.route('/activeUsers', methods = ['POST'])
@cross_origin()
def activeUsers():
    uid = request.json['uid']
    print(uid)
    users = getFollowingUsers(uid)
    print(users)
    user_string = ""
    for key in users:
        user_string += key + ';' + users[key] + ','
    return str(user_string)[:-1]

@app.route('/update', methods = ['POST'])
@cross_origin()
def update():
    return "update not yet implemented"

@app.route('/createFriendPlaylist', methods = ['POST'])
@cross_origin()
def createFriendPlaylist():
    userID = request.json['userID']
    friendID = request.json['friendID']
    resp = buildPlaylistFromFriendData(userID, friendID)
    playlist = ""
    for tup in resp:
        playlist += tup[1] + '` ' + tup[2] + '` ' + tup[3]
        if tup != resp[-1]:
            playlist += ';'
    return str(playlist)

@app.route('/deleteUser', methods = ['POST'])
@cross_origin()
def deleteUser():
    tokenData = request.json['token']
    deleteUserRecentlyPlayed(tokenData)
    return "delete completed"

@app.route('/demoQuery', methods = ['POST'])
@cross_origin()
def demoQuery():
    tokenData = request.json['token']
    print(getRecentlyListened(tokenData))
    return str(getRecentlyListened(tokenData))

@app.route('/updateFollow', methods = ['POST'])
@cross_origin
def updateFollow():
    tokenData  = request.json['token']
    updateFollows()
    return "follow updated"

@app.route('/addPlaylistToLibrary', methods = ['POST'])
@cross_origin()
def addPlaylistToLibrary():
    tokenData = request.json['token']
    uriList = request.json['uris']
    name = request.json['name']
    print(tokenData, uriList)
    addPlaylist(tokenData, uriList, name)
    return "playlist added"

@app.route('/createAllFollowingPlaylist', methods = ['POST'])
@cross_origin()
def createAllFollowingPlayist():
    tokenData = request.json['token']
    resp = buildPlaylistAllFollowing(tokenData)
    playlist = ""
    for tup in resp:
        playlist += tup[1] + '` ' + tup[2] + '` ' + tup[3]
        if tup != resp[-1]:
            playlist += ';'
    return str(playlist)

@app.route('/addAllFollowingPlaylist', methods = ['POST'])
@cross_origin()
def addAllFollowingPlaylist():
    tokenData = request.json['token']
    uriList = request.json['uris']
    name = request.json['name']
    print(tokenData, uriList)
    addPlaylist(tokenData, uriList, name)
    return "playlist added"

@app.route('/getRecommendedPodcasts', methods = ['POST'])
@cross_origin()
def getRecommendedPodcasts():
    userID = request.json['uid']
    podcastList = findRecommendedShows(userID)
    print(str(podcastList))
    showNames = getShowNames(podcastList)
    podcaststr = ""
    for show in showNames:
        podcaststr += show
        if show != showNames[-1]:
            podcaststr += '`'
    return str(podcaststr)

app.run(port = 5000, host = "0.0.0.0")