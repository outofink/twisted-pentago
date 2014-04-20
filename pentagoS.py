from os import system, name

class Pentago:
	def __init__(self):
		self.play()

	def genBoard(self):
		x = [[" "]*9]*4
		return x

	def prettyBoard(self, board):
		mboard = """\
	{0[0][0]} {0[0][1]} {0[0][2]}|{0[1][0]} {0[1][1]} {0[1][2]}
	{0[0][3]} {0[0][4]} {0[0][5]}|{0[1][3]} {0[1][4]} {0[1][5]}
	{0[0][6]} {0[0][7]} {0[0][8]}|{0[1][6]} {0[1][7]} {0[1][8]}
	-----+-----
	{0[2][0]} {0[2][1]} {0[2][2]}|{0[3][0]} {0[3][1]} {0[3][2]}
	{0[2][3]} {0[2][4]} {0[2][5]}|{0[3][3]} {0[3][4]} {0[3][5]}
	{0[2][6]} {0[2][7]} {0[2][8]}|{0[3][6]} {0[3][7]} {0[3][8]}""".format(board)
		return mboard

	def rotateCC(self, board, sector):
		nboard=self.genBoard()
		for x in range(4):
			if x != sector:
				nboard[x]=board[x]
		nboard[sector][0] = board[sector][2]
		nboard[sector][1] = board[sector][5]
		nboard[sector][2] = board[sector][8]
		nboard[sector][3] = board[sector][1]
		nboard[sector][4] = board[sector][4]
		nboard[sector][5] = board[sector][7]
		nboard[sector][6] = board[sector][0]
		nboard[sector][7] = board[sector][3]
		nboard[sector][8] = board[sector][6]
		return nboard

	def rotateC(self, board, sector):
		nboard=self.genBoard()
		for x in range(4):
			if x != sector:
				nboard[x]=board[x]
		nboard[sector][2] = board[sector][0]
		nboard[sector][5] = board[sector][1]
		nboard[sector][8] = board[sector][2]
		nboard[sector][1] = board[sector][3]
		nboard[sector][4] = board[sector][4]
		nboard[sector][7] = board[sector][5]
		nboard[sector][0] = board[sector][6]
		nboard[sector][3] = board[sector][7]
		nboard[sector][6] = board[sector][8]
		return nboard

	def printBoard(self, board, spacing=0):
		system('cls' if name == 'nt' else 'clear')
		print self.prettyBoard(board)
		print

	def rotateSquare(self, board):
		while True:
			pass0 = False
			pass1 = False
			pass2 = False
			rawrot=raw_input("Rotation (ie. A' or C\"): ")
			if rawrot== " ":
				return board
			if len(rawrot) == 2:
				pass0 = True
			if pass0:
				for x in ["'",'"']:
					if rawrot.endswith(str(x)):
						pass1 = True
				for x in ["A", "B", "C", "D"]:
					if rawrot.startswith(x):
						pass2 = True
			if pass1 and pass2:
				if rawrot.startswith("A"):
					square = 0
				elif rawrot.startswith("B"):
					square = 1
				elif rawrot.startswith("C"):
					square = 2
				else:
					square = 3
				if rawrot.endswith("'"):
					return self.rotateC(board, square)
				else:
					return self.rotateCC(board, square)
	def placePiece(self, board, color):
		pass3 = False
		while pass3 == 0:
			pass0 = False
			pass1 = False
			pass2 = False
			rawloc=raw_input("Location (ie. A4 or C9): ")
			if len(rawloc) == 2:
				pass0 = True
			if pass0:
				for x in range(1,10):
					if rawloc.endswith(str(x)):
						pass1 = True
				for x in ["A", "B", "C", "D"]:
					if rawloc.startswith(x):
						pass2 = True
			if pass1 and pass2:
				if rawloc.startswith("A"):
					square = 0
				elif rawloc.startswith("B"):
					square = 1
				elif rawloc.startswith("C"):
					square = 2
				else:
					square = 3
				place=int(rawloc[-1])
				if board[square][place-1]==" ":
					pass3 = True

		nboard=self.genBoard()
	
		nboard[square][place-1] = color
		for x in range(4):
			if x != square:
				nboard[x]=board[x]
		return nboard


	def winBoards(self, board):
		hboard = [board[0][:3]  + board[1][:3] , \
				  board[0][3:6] + board[1][3:6], \
				  board[0][6:]  + board[1][6:],  \
				  board[2][:3]  + board[3][:3] , \
				  board[2][3:6] + board[3][3:6], \
				  board[2][6:]  + board[3][6:]]

		vboard = [board[0][0::3] + board[2][0::3] , \
				  board[0][1::3] + board[2][1::3], \
				  board[0][2::3] + board[2][2::3], \
				  board[1][0::3] + board[3][0::3] , \
				  board[1][1::3] + board[3][1::3], \
				  board[1][2::3] + board[3][2::3]]

		dboard = [board[1][:8][2::2] + board[2][:8][2::2], \
				  board[0][0::4]     + board[3][0::4]]

		triboard = [board[0][3::4] + [board[2][2]] + board[3][3::4], \
		            board[0][1::4] + [board[1][6]] + board[3][1::4], \
		            board[1][:4][1::2] + [board[0][8]] + board[2][:4][1::2], \
		            board[1][5::2] + [board[3][0]] + board[2][5::2]]
		return [hboard, vboard, dboard, triboard]

	def checkGameOver(self, boards):
		winners =[]
		for x in boards:
			for y in range(len(x)):
				#result_list = []
				current = x[y][0]
				count = 0
				for value in x[y]:
				    if value == current:
				        count += 1
				    else:
				        #result_list.append((current, count))
				        if count >= 5 and current != " ":
				        	winners.append(current)
				        current = value
				        count = 1
				#result_list.append([current, count])
				if count >= 5 and current != " ":
				    winners.append(current)
		if "B" in winners and "W" in winners:
			return "BW"
		elif "B" in winners:
			return "B"
		elif "W" in winners:
			return "W"
		return None

	def prettyCheckGameover(self, board):
		CGO=self.checkGameOver(self.winBoards(board))
		if CGO == "B":
			print "Black wins! Good game!"
			return True
		elif CGO == "W":
			print "White wins! Good game!"
			return True
		elif CGO == "BW":
			print "It's a tie! Good game!"
			return True
		over = True
		for x in range(4):
			for y in board[x]:
				if y == " ":
					over = False
		if over:
			print "It's a tie! Good game!"
			return True

		return False

	def play(self):
		system('cls' if name == 'nt' else 'clear')
		gameBoard=self.genBoard()
		playing = True
		self.printBoard(gameBoard)
		while playing:
			#white's turn
			print "White's Turn\n"
			gameBoard=self.placePiece(gameBoard, "W")
			self.printBoard(gameBoard)
			if self.prettyCheckGameover(gameBoard):
				playing = False
			if playing:
				print "White's Turn\n"
				gameBoard=self.rotateSquare(gameBoard)
				self.printBoard(gameBoard)
				if self.prettyCheckGameover(gameBoard):
					playing = False
				if playing:
					print "Blacks's Turn\n"
					gameBoard=self.placePiece(gameBoard, "B")
					self.printBoard(gameBoard)
					if self.prettyCheckGameover(gameBoard):
						playing = False
					if playing:
						print "Blacks's Turn\n"
						gameBoard=self.rotateSquare(gameBoard)
						self.printBoard(gameBoard)
						if self.prettyCheckGameover(gameBoard):
							playing = False
new_game=Pentago()
new_game()
