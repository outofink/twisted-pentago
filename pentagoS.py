import numpy as np

class Pentago:
    def __init__(self):
        self.player = 1
        self.playing = True
        self.placing = True
        self.gameBoard = np.full([4, 9], " ")

        self.ps = {1:"W", 2:"B"}
        self.players = {1: "White", 2: "Black"}
        self.sectors = {"A": 0, "B": 1, "C": 2, "D": 3}
        self.numbers = [str(i) for i in range(1, 10)]
        self.direction = {"'": -1, '"': 1}

    def switchPlayers(self):
        self.player = 3 - self.player

    def get2dArray(self):
        quad = []
        for quadrant in self.gameBoard:
            quad.append(quadrant.reshape(3,3))
        return np.hstack((np.vstack((quad[0],quad[2])), np.vstack((quad[1], quad[3]))))

    def get1dArray(self):
        return self.get2dArray().flatten()

    def printBoard(self):
        #make 2d array of each corner
        board = self.get1dArray()

        prettyBoard = """\
        {} {} {}|{} {} {}
        {} {} {}|{} {} {}
        {} {} {}|{} {} {}
        -----+-----
        {} {} {}|{} {} {}
        {} {} {}|{} {} {}
        {} {} {}|{} {} {}
        """.format(*board)

        print("\033[H\033[J") # clears the screen
        print(prettyBoard)

    def rotate(self, sector, direction):
        self.gameBoard[sector] = np.rot90(self.gameBoard[sector].reshape(3,3), direction).flatten()

    def place(self, position, player):
        self.gameBoard[position["letter"]][position["number"]] = player

    def rotateSquare(self):
        print("{}'s Turn".format(self.players[self.player]))
        while True:
            rawRot = input("Rotation (e.g. A' or C\"): ")
            if self.cleanRotation(rawRot):
                rot = self.formattedRotation(rawRot)
                self.rotate(rot["letter"], rot["direction"])
                self.printBoard()
                return

    def placePiece(self):
        print("{}'s Turn".format(self.players[self.player]))
        while True:
            rawLoc = input("Location (e.g. A4 or C9): ")
            if self.cleanLocation(rawLoc):
                pos = self.formattedLocation(rawLoc)
                self.place(pos, self.ps[self.player])
                self.printBoard()
                return

    def cleanLocation(self, loc):
        if len(loc) != 2:
            return False
        if loc[0].upper() not in self.sectors:
            return False
        if loc[1] not in self.numbers:
            return False
        if self.gameBoard[self.sectors[loc[0].upper()]][int(loc[1]) - 1] != " ":
            return False
        return True

    def cleanRotation(self, rot):
        if len(rot) != 2:
            return False
        if rot[0].upper() not in self.sectors:
            return False
        if rot[1] not in self.direction:
            return False
        return True

    def formattedLocation(self, loc):
        letter = self.sectors[loc[0].upper()]
        number = int(loc[1]) - 1
        return {"letter": letter, "number": number}

    def formattedRotation(self, rot):
        letter = self.sectors[rot[0].upper()]
        direction = self.direction[rot[1]]
        return {"letter": letter, "direction": direction}

    def winBoards(self):
        board = self.get2dArray()

        rows = board.tolist()
        columns = np.rot90(board).tolist()
        diagPos = [board.diagonal(x).tolist() for x in range(-1,2)]
        diagNeg = [np.fliplr(board).diagonal(x).tolist() for x in range(-1,2)]

        return (rows + columns + diagNeg + diagPos)

    def checkGameOver(self):
        boards = self.winBoards()
        winners = []
        for board in boards:
            s = ''.join(board)
            for player in self.ps.values():
                if s.find(player * 5) >= 0:
                    winners.append(player)
                    self.playing = False

        if "B" in winners and "W" in winners:
            print("It's a tie! Good game!")
        elif "B" in winners:
            print("Black wins! Good game!")
        elif "W" in winners:
            print("White wins! Good game!")

        #check if the board's full
        if not " " in self.gameBoard and self.playing:
            print("All full! It's a tie! Good game!")
            self.playing = False

    def play(self):
        self.printBoard()
        while self.playing:
            self.placePiece()
            self.rotateSquare()
            self.switchPlayers()
            self.printBoard()
            self.checkGameOver()

if __name__ == "__main__":
    Pentago().play()
