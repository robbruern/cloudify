from flask import Flask, request
from flask_cors import CORS, cross_origin
from spotifyRequests import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route('/token', methods = ['POST'])
@cross_origin()
def token():
    print(request)
    tokenData = request.json['token']
    userID = getUserID(tokenData)
    userName = getUsername(tokenData)
    print(userID, userName)
    insert_user(userID, userName)
    getTopTracks(tokenData)
    updateFollows(tokenData)
    return userName

@app.route('/activeUsers', methods = ['GET'])
@cross_origin()
def activeUsers():
    users = (retrieve_active_users())
    user_string = ""
    for user in users:
        user_string += user[0] + ';' + user[1]
        if user != users[-1]:
            user_string += ','
    return str(user_string)

@app.route('/update', methods = ['POST'])
@cross_origin()
def update():
    return "update not yet implemented"

@app.route('/createPlaylist', methods = ['POST'])
@cross_origin()
def createPlaylist():
    friendID = request.json['friendID']
    resp = build_friends_recommended_playlist(friendID, 20)
    return str(resp)

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
    addPlaylist()
    return "playlist added"

app.run(port = 5000, host = "0.0.0.0")