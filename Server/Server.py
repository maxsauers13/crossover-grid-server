class Server:
    def __init__(self, mongo_db_guess):
        self.encoding_standard = "utf-8"
        self.mongo_db_guess = mongo_db_guess
    
    # save a guess in mongo db
    def saveGuess(self, player, team1, team2, correct):
        document = {
            "player": player,
            "team1": team1,
            "team2": team2,
            "correct": correct
        }

        result = self.mongo_db_guess.insert_one(document)
        if result.acknowledged:
            return True, f"Guess saved: {player} - {team1} - {team2}"
        else:
            return False, "Database not acknowledged"

    # get the rarity of a guess
    # def guessRarity(self, player, team1, team2):
    #     # find number of times player has guessed
    #     query = {'$and': [
    #         {'player': player},
    #         {'team1': team1},
    #         {'team2': team2}
    #     ]}
    #     playerGuesses = self.mongo_db_guess.find(query)

        # find total number of guesses for 2 team combos