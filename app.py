from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from Server.Server import Server
import json

app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
# Configure SSL/TLS certificate and private key paths
ssl_cert = '/etc/letsencrypt/live/crossovergridserver.com/fullchain.pem'
ssl_key = '/etc/letsencrypt/live/crossovergridserver.com/privkey.pem'

mongo_client = MongoClient("mongodb+srv://jared:kyhzur-Xokson-4netru@crossovergrid.1o3jktx.mongodb.net/?retryWrites=true&w=majority")
mongo_db_guess = mongo_client["CrossoverGrid"]["Guess"]
server = Server(mongo_db_guess)

####################################################END POINTS#######################################################

@app.route("/guess/save", methods=["POST"])
@cross_origin()
def saveGuess():
    body = json.loads(request.data.decode(server.encoding_standard))
    player = body.get("player")
    team1 = body.get("team1")
    team2 = body.get("team2")
    correct = body.get("correct")

    success, response = server.saveGuess(player, team1, team2, correct)
    return response if success else Response(status=400, response=response)

@app.route("/guesses/fetch/<numGuesses>", methods=["GET"])
@cross_origin()
def fetchGuesses(numGuesses):
    success, response = server.fetchGuesses()
    return response if success else Response(status=400, response=response)

if __name__ == "__main__":
    # app.run(host="34.136.209.112", port=41454, debug=True)
    app.run(ssl_context=(ssl_cert, ssl_key))