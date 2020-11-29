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
    userID = getUserID(tokenData)
    userName = getUsername(tokenData)
    print(userID, userName)
    insert_user(userID, userName)
    return "User Verified and Added to Active Users"

@app.route('/activeUsers', methods = ['GET'])
@cross_origin()
def activeUsers():
    users = (retrieve_active_users())
    user_string = ""
    for user in users:
        user_string += user
        if user != users[-1]:
            user_string += ','
    return str(user_string)

@app.route('/update', methods = ['POST'])
@cross_origin()
def update():
    return "update not yet implemented"

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

app.run(port = 5000, host = "0.0.0.0")