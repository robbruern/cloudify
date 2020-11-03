from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route('/token', methods = ['POST'])
@cross_origin()
def token():
    print(request.json)
    return "penis"


app.run(port = 5000, host = "0.0.0.0")