import os # only to clear the screen

class Pentago:
	def __init__(self):
		self.player = 1
		self.playing = True
		self.placing = True
		self.gameBoard = [[" " for i in range(9)] for j in range(4)]

		self.ps = {1:"W", 2:"B"}
		self.players = {1: "White", 2: "Black"}

	def switchPlayers(self):
		self.player = 3 - self.player

	def get2dArray(self):
		#make 2d array of each corner
		corner = []

		for x in range(4):
			corner.append([self.gameBoard[x][i:i + 3] for i in range(0, len(self.gameBoard[x]), 3)])
		
		#make and fill 2d array of the whole board
		board = []

		for i in range(0,3,2):
			for j in range(3):
				board.append(corner[i][j] + corner[i+1][j])
		return board

	def get1dArray(self):
		array = self.get2dArray()
		board = []
		
		for row in array:
			board += row
		return board

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
		#get corner and convert it to 2d array
		corner2 = [self.gameBoard[sector][i:i + 3] for i in range(0, len(self.gameBoard[sector]), 3)]
		#rotate corner
		if clockwise:
			rotatedCorner2 = list(zip(*corner2[::-1]))
		else:
			rotatedCorner2 = list(zip(*corner2))[::-1]
		#convert back to 1d array
		corner = [j for i in rotatedCorner2 for j in i]
		#add the corner back
		self.gameBoard[sector] = corner

	def rotateSquare(self):
		sectors = {"A": 0, "B": 1, "C": 2, "D": 3}
		clockwise = {"'": True, '"': False}
		while True:
			rawRot = input("Rotation (e.g. A' or C\"): ")
			if len(rawRot) == 2:
				if (rawRot[0] in sectors) and (rawRot[1] in clockwise):
					self.rotate(sectors[rawRot[0]], clockwise[rawRot[1]])
					self.placing = True
					return

	def placePiece(self):
		sectors = {"A": 0, "B": 1, "C": 2, "D": 3}
		numbers = [str(i) for i in range(1, 10)]
		while True:
			rawLoc = input("Location (e.g. A4 or C9): ")
			if len(rawLoc) == 2:
				if (rawLoc[0] in sectors) and (rawLoc[1] in numbers):
					if self.gameBoard[sectors[rawLoc[0]]][int(rawLoc[1]) - 1] == " ":
						self.gameBoard[sectors[rawLoc[0]]][int(rawLoc[1]) - 1] = self.ps[self.player]
						self.placing = False
						return

	def diagonalsPos(self, matrix):
		#Get positive diagonals, going from bottom-left to top-right.
		result = []
		for di in ([(j, i - j) for j in range(6)] for i in range(11)):
			result.append([matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < 6 and j < 6])
		return result

	def diagonalsNeg(self, matrix):
		#Get negative diagonals, going from top-left to bottom-right.
		result = []
		for di in ([(j, i + j - 5) for j in range(6)] for i in range(11)):
			result.append([matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < 6 and j < 6])
		return result

	def winBoards(self):
		board = self.get2dArray()

		rows = board
		columns = list(zip(*board))
		diagPos = self.diagonalsPos(board)
		diagNeg = self.diagonalsNeg(board)

		return (rows + columns + diagNeg + diagPos)

	def checkGameOver(self):
		boards = self.winBoards()
		winners = []
		for board in boards:
			first = ""
			count = 0
			for place, i in enumerate(board):
				if board[place] == first:
					count += 1
				else:
					first = board[place]
					count = 1
				if count >= 5 and board[place] != " ":
					winners.append(board[place])
					self.playing = False

		if "B" in winners and "W" in winners:
			print("It's a tie! Good game!")
		elif "B" in winners:
			print("Black wins! Good game!")
		elif "W" in winners:
			print("White wins! Good game!")

		#check if the board's full
		full = True
		for corner in self.gameBoard:
			for place in corner:
				if place == " ":
					full = False
		if full and self.playing:
			print("It's a tie! Good game!")
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
