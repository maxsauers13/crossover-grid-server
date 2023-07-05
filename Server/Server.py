from datetime import datetime

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
            "correct": correct,
            "day": datetime.now().strftime("%Y-%m-%d")
        }

        result = self.mongo_db_guess.insert_one(document)

        # get percentage if correct guess
        rarity = None
        if correct:
            rarity = self.guessRarity(player, team1, team2)
        else:
            print(player, team1, team2, "incorrect")

        if result.acknowledged:
            return True, {"rarity": rarity}
        else:
            return False, "Database not acknowledged"

    # get the rarity of a guess
    def guessRarity(self, player, team1, team2):
        # find number of times player has guessed
        queryPlayer = {'$and': [
            {'player': player},
            {'team1': team1},
            {'team2': team2}
        ]}
        playerGuesses = list(self.mongo_db_guess.find(queryPlayer))

        # find total number of guesses for 2 team combo
        queryTeams = {'$and': [
            {'team1': team1},
            {'team2': team2},
            {"correct": True}
        ]}
        teamGuesses = list(self.mongo_db_guess.find(queryTeams))

        # calculate rarity
        rarity = int((len(playerGuesses) / len(teamGuesses)) * 100)
        print(player, team1, team2, len(playerGuesses), len(teamGuesses), rarity)
        return rarity