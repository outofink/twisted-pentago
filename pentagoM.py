#!c:/Python27/python.exe -u
import server
import gamedb

class Pentago():
	
	def __init__(self, cid1, cid2):
		self.cid = {1: cid1, 2: cid2}
		self.active = 1 #player number
		gamedb.create_game(cid1, cid2)
		self._get_next_init([0,]*36)

	def move_received(self, move):
		print('received:', move)
		#does the move on the server:
		gamedb.make_move(self.cid[self.active], self.active, move)
		#sends back dirty board
		state = gamedb.get_state(self.cid[self.active])
		print(state)
		print('new state:', state)
		#check to see if game has been won:
		winner = self._winner(state)
		#if not:
		if winner == 0:
			self.active = 3 - self.active
			#get next (same)
			print("shown to other")
			self._get_next_shown(state)
		elif winner == -1:
			gamedb.game_over(self.cid[1], 1, True) # mark game as a draw
			server.game_over(self.cid[1], self.cid[2], True, state)
		else:
			gamedb.game_over(self.cid[winner], winner, False)
			server.game_over(self.cid[winner], self.cid[3-winner], False, state)

	def rotate_received(self, rotate):
		print('received:', rotate)
		#does the rotate on the server:
		gamedb.make_rotate(self.cid[self.active], self.active, rotate)
		#sends back dirty board
		state = gamedb.get_state(self.cid[self.active])
		print(state)
		print('new state:', state)
		#check to see if game has been won:
		winner = self._winner(state)
		#if not:
		if winner == 0:
			print("move to other")
			self.active = 3 - self.active
			#get next
			self._get_next_move(state)
		elif winner == -1:
			gamedb.game_over(self.cid[1], 1, True) # mark game as a draw
			server.game_over(self.cid[1], self.cid[2], True, state)
		else:
			gamedb.game_over(self.cid[winner], winner, False)
			server.game_over(self.cid[winner], self.cid[3-winner], False, state)
	
	def shown_received(self, shown):
		print('received:', shown)
		print("rotate to other")
		state = gamedb.get_state(self.cid[self.active])
		self.active = 3 - self.active
		self._get_next_rotate(state)

	def init_received(self, init):
		print('received:', init)
		print("move to other")
		state = [0,]*36
		self.active = 3 - self.active
		self._get_next_move(state)

	def err_received(self):
		raise Exception('Errback called')
	
	def _get_next_move(self, state):
		d = server.get_move_from(self.cid[self.active], state)
		d.addCallbacks(self.move_received, self.err_received)

	def _get_next_rotate(self, state):
		d = server.get_rotate_from(self.cid[self.active], state)
		d.addCallbacks(self.rotate_received, self.err_received)

	def _get_next_shown(self, state):
		d = server.get_shown_from(self.cid[self.active], state)
		d.addCallbacks(self.shown_received, self.err_received)

	def _get_next_init(self, state):
		d = server.get_init_from(self.cid[self.active], state)
		d.addCallbacks(self.init_received, self.err_received)
	
	def _winner(self, state):

		board=[list(state[:9]), list(state[9:18]), list(state[18:27]), list(state[27:36])]
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
		boards = [hboard, vboard, dboard, triboard]
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
				        if count >= 5 and current != 0:
				        	winners.append(current)
				        current = value
				        count = 1
				#result_list.append([current, count])
				if count >= 5 and current != 0:
				    winners.append(current)
		if 1 in winners and 2 in winners:
			return -1
		elif 1 in winners:
			return 1
		elif 2 in winners:
			return 2
		for x in range(4):
			if not 0 in board[x]:
				return -1
		return 0

if __name__ == '__main__':
	server.run(Pentago)
