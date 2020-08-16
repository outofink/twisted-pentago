import numpy as np


class Pentago:
    def __init__(self):
        self.player = 1
        self.playing = True
        self.placing = True
        self.gameBoard = np.full([4, 9], " ")

        self.ps = {1: "W", 2: "B"}
        self.players = {1: "White", 2: "Black"}
        self.sectors = {"A": 0, "B": 1, "C": 2, "D": 3}
        self.numbers = [str(i) for i in range(1, 10)]
        self.direction = {"'": -1, '"': 1}

    def switch_players(self):
        self.player = 3 - self.player

    def get_2d_array(self):
        quad = []
        for quadrant in self.gameBoard:
            quad.append(quadrant.reshape(3, 3))
        return np.hstack((np.vstack((quad[0], quad[2])), np.vstack((quad[1], quad[3]))))

    def get_1d_array(self):
        return self.get_2d_array().flatten()

    def print_board(self):
        # make 2d array of each corner
        board = self.get_1d_array()

        pretty_board = """\
        {} {} {}|{} {} {}
        {} {} {}|{} {} {}
        {} {} {}|{} {} {}
        -----+-----
        {} {} {}|{} {} {}
        {} {} {}|{} {} {}
        {} {} {}|{} {} {}
        """.format(*board)

        print("\033[H\033[J")  # clears the screen
        print(pretty_board)

    def rotate(self, sector, direction):
        self.gameBoard[sector] = np.rot90(self.gameBoard[sector].reshape(3, 3), direction).flatten()

    def place(self, position, player):
        self.gameBoard[position["letter"]][position["number"]] = player

    def rotate_square(self):
        print("{}'s Turn".format(self.players[self.player]))
        while True:
            raw_rotation = input("Rotation (e.g. A' or C\"): ")
            if self.is_valid_rotation(raw_rotation):
                rot = self.formatted_rotation(raw_rotation)
                self.rotate(rot["letter"], rot["direction"])
                self.print_board()
                return

    def place_piece(self):
        print("{}'s Turn".format(self.players[self.player]))
        while True:
            raw_location = input("Location (e.g. A4 or C9): ")
            if self.is_valid_location(raw_location):
                pos = self.formatted_location(raw_location)
                self.place(pos, self.ps[self.player])
                self.print_board()
                return

    def is_valid_location(self, location):
        if len(location) != 2:
            return False
        if location[0].upper() not in self.sectors:
            return False
        if location[1] not in self.numbers:
            return False
        if self.gameBoard[self.sectors[location[0].upper()]][int(location[1]) - 1] != " ":
            return False
        return True

    def is_valid_rotation(self, rotation):
        if len(rotation) != 2:
            return False
        if rotation[0].upper() not in self.sectors:
            return False
        if rotation[1] not in self.direction:
            return False
        return True

    def formatted_location(self, location):
        letter = self.sectors[location[0].upper()]
        number = int(location[1]) - 1
        return {"letter": letter, "number": number}

    def formatted_rotation(self, rotation):
        letter = self.sectors[rotation[0].upper()]
        direction = self.direction[rotation[1]]
        return {"letter": letter, "direction": direction}

    def potential_win_layouts(self):
        board = self.get_2d_array()

        rows = board.tolist()
        columns = np.rot90(board).tolist()
        diagonal1 = [board.diagonal(x).tolist() for x in range(-1, 2)]
        diagonal2 = [np.fliplr(board).diagonal(x).tolist() for x in range(-1, 2)]

        return [*rows, *columns, *diagonal1, *diagonal2]

    def check_gameover(self):
        boards = self.potential_win_layouts()
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

        # check if the board's full
        if " " not in self.gameBoard and self.playing:
            print("All full! It's a tie! Good game!")
            self.playing = False

    def play(self):
        self.print_board()
        while self.playing:
            self.place_piece()
            self.rotate_square()
            self.switch_players()
            self.print_board()
            self.check_gameover()


if __name__ == "__main__":
    Pentago().play()
