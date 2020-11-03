from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/token', methods = ['POST'])
def token():
    print(request.json)
    return "penis"

app.run()