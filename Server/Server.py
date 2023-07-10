from datetime import datetime, timezone, timedelta
import time

class Server:
    def __init__(self, mongo_db_guess, mongo_db_grid, mongo_db_guessPercentage):
        self.encoding_standard = "utf-8"
        self.mongo_db_guess = mongo_db_guess
        self.mongo_db_guessPercentage = mongo_db_guessPercentage
        self.mongo_db_grid = mongo_db_grid
    
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
            # rarity = self.guessRarity(player, team1, team2)
            queryPlayer = {'$and': [
                {'player': player},
                {'team1': team1},
                {'team2': team2}
            ]}
            playerGuessed = self.mongo_db_guessPercentage.find_one(queryPlayer)

            if not playerGuessed:
                document = {
                    "player": player,
                    "team1": team1,
                    "team2": team2
                }
                self.mongo_db_guessPercentage.insert_one(document)
                playerGuessed = self.mongo_db_guessPercentage.find_one(queryPlayer)

            # determine if percentage needs to be updated
            if playerGuessed != None and ("rarity" not in playerGuessed or "datetime" not in playerGuessed or datetime.fromtimestamp(time.time(), tz=timezone.utc) - playerGuessed["datetime"] >= timedelta(minutes=10)):
                rarity = self.updateRarity(player, team1, team2)
        # else:
            # print(player, team1, team2, "incorrect")

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
        # playerGuesses = list(self.mongo_db_guess.find(queryPlayer))
        playerGuesses = self.mongo_db_guess.count_documents(queryPlayer)

        # find total number of guesses for 2 team combo
        queryTeams = {'$and': [
            {'team1': team1},
            {'team2': team2},
            {"correct": True}
        ]}
        # teamGuesses = list(self.mongo_db_guess.find(queryTeams))
        teamGuesses = self.mongo_db_guess.count_documents(queryTeams)

        # calculate rarity
        # rarity = round((len(playerGuesses) / len(teamGuesses)) * 100, 1)
        rarity = round((playerGuesses / teamGuesses) * 100, 1)
        # print(player, team1, team2, playerGuesses, teamGuesses, rarity)
        return rarity

    def updateRarity(self, player, team1, team2):
        rarity = self.guessRarity(player, team1, team2)
        queryPlayer = {'$and': [
            {'player': player},
            {'team1': team1},
            {'team2': team2}
        ]}

        updateValues = {"$set": {"rarity": rarity, "datetime": datetime.fromtimestamp(time.time(), tz=timezone.utc)}}

        self.mongo_db_guessPercentage.update_one(queryPlayer, updateValues)
        print(player, team1, team2, rarity)
        return rarity

    # save a grid and gets its rank
    def saveGrid(self, teams, players, score):
        document = {
            "teams": teams,
            "score": score
        }

        result = self.mongo_db_grid.insert_one(document)

        # get rank
        rank, total = self.gridRank(document)
        print(f"Grid score {score} is rank {rank}")

        if result.acknowledged:
            return True, {"rank": rank, "total": total}
        else:
            return False, "Database not acknowledged"

    # get the rank of the grid
    def gridRank(self, document):
        higherScoreCount = self.mongo_db_grid.count_documents({
            "teams": document["teams"],
            "score": {"$lt": document["score"]}
        })

        totalScoreCount = self.mongo_db_grid.count_documents({
            "teams": document["teams"]
        })

        return higherScoreCount + 1, totalScoreCount

    # fetch the n most recent guesses
    def fetchGuesses(self, numGuesses):
        guesses = list(self.mongo_db_guess.find({}, {"_id:": 0}).sort('_id', -1).limit(int(numGuesses)))
        guesses = [guess["player"] + " " + guess["team1"] + " " + guess["team2"] for guess in guesses]
        # print(guesses)
        return True, guesses