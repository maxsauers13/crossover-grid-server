from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from server.Server import Server
import json

app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

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

    success, response = server.saveGuess(player, team1, team2)
    return response if success else Response(status=400, response=response)