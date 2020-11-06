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
    addRecentlyListened(tokenData)
    return "penis"

@app.route('/update', methods = ['POST'])
@cross_origin()
def update():
    return "update not yet implemented"

@app.route('/deleteUser', methods = ['POST'])
@cross_origin()
def deleteUser():
    tokenData = request.json['token']
    deleteUser(tokenData)
    return "delete completed"

app.run(port = 5000, host = "0.0.0.0")