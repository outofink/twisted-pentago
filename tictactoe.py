import server
import gamedb

class TicTacToe():
	
	def __init__(self, cid1, cid2):
		self.cid = {1: cid1, 2: cid2}
		self.active = 1
		gamedb.create_game(cid1, cid2)
		self._get_next_move((0,)*9)

	
	def move_received(self, move):
		print 'received:', move
		gamedb.make_move(self.cid[self.active], self.active, move)
		state = gamedb.get_state(self.cid[self.active])
		print 'new state:', state
		winner = self._winner(state, move)
		if winner == 0:
			self.active = 3 - self.active
			self._get_next_move(state)
		elif winner == -1:
			gamedb.game_over(self.cid[1], 1, True) # mark game as a draw
			server.game_over(self.cid[1], self.cid[2], True, state)
		else:
			gamedb.game_over(self.cid[winner], winner, False)
			server.game_over(self.cid[winner], self.cid[3-winner], False, state)
			

	def err_received(self):
		raise Exception('Errback called')

	
	def _get_next_move(self, state):
		d = server.get_move_from(self.cid[self.active], state)
		d.addCallbacks(self.move_received, self.err_received)

	
	def _winner(self, state, move):
		# Check verticals
		if state[move] == state[move-3] == state[move-6]:
			return state[move]
		# Check horizontals
		row = 3 * (move / 3)
		if state[row] == state[row+1] == state[row+2]:
			return state[row]
		# Check diagonals
		if state[0] == state[4] == state[8] or state[2] == state[4] == state[6]:
			return state[4]
		# Check draw
		if not 0 in state:
			return -1
		# No winner
		return 0




### Main External Call ###

if __name__ == '__main__':
	server.run(TicTacToe)