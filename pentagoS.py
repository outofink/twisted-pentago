import os # only to clear the screen
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
		self.clockwise = {"'": -1, '"': 1}

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

		os.system('cls' if os.name == 'nt' else 'clear')
		print(prettyBoard)

	def rotate(self, sector, clockwise):
		self.gameBoard[sector] = np.rot90(self.gameBoard[sector].reshape(3,3), clockwise).flatten()

	def rotateSquare(self):
		while True:
			rawRot = input("Rotation (e.g. A' or C\"): ")
			if (len(rawRot) == 2) and (andrawRot[0] in self.sectors) and (rawRot[1] in self.clockwise):
				self.rotate(self.sectors[rawRot[0]], self.clockwise[rawRot[1]])
				self.placing = True
				return

	def placePiece(self):
		numbers = [str(i) for i in range(1, 10)]
		while True:
			rawLoc = input("Location (e.g. A4 or C9): ")
			if (len(rawLoc) == 2) and (rawLoc[0] in self.sectors) and (rawLoc[1] in numbers):
				if self.gameBoard[self.sectors[rawLoc[0]]][int(rawLoc[1]) - 1] == " ":
					self.gameBoard[self.sectors[rawLoc[0]]][int(rawLoc[1]) - 1] = self.ps[self.player]
					self.placing = False
					return

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
			print("{}'s Turn".format(self.players[self.player]))
			if self.placing:
				self.placePiece()
			else:
				self.rotateSquare()
				self.switchPlayers()

			self.printBoard()
			self.checkGameOver()

if __name__ == "__main__":
	Pentago().play()
