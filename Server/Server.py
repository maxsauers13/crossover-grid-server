class Server:
    def __init__(self, mongo_db_guess):
        self.mongo_db_guess = mongo_db_guess
    
    # save a guess in mongo db
    def saveGuess(self, player, team1, team2):
        document = {
            "player": player,
            "team1": team1,
            "team2": team2
        }

        result = self.mongo_db_guess.insert_one(document)
        if result.acknowledged:
            return True, f"Guess saved: {player} - {team1} - {team2}"
        else:
            return False, "Database not acknowledged"