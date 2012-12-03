from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import defer, reactor
import json

class GameProtocol(Protocol):

	active = False
	deferred = None

	def dataReceived(self, data):
		msg = json.loads(data)
		if 'type' not in msg:
			self._send_error('Received improper message')
		elif msg['type'] == 'move':
			if self.active:
				self.deferred.callback( msg['value'] )
				self.deferred = None
				self.active = False
			else:
				self._send_error('Not your turn yet')
		else:
			self._send_error('Received unknown message type')

	def prompt_for_move(self, game_state, d):
		self.active = True
		self.deferred = d
		data_out = dict(type='prompt', value='move', state=game_state)
		self.transport.write(json.dumps(data_out))

	def game_over(self, is_winner, game_state):
		data_out = dict(type='winner', value=is_winner, state=game_state)
		self.transport.write(json.dumps(data_out))
		self.transport.loseConnection()

	def _send_error(self, msg):
		data_out = dict(type='error', value=msg)
		self.transport.write(json.dumps(data_out))



class GameFactory(ServerFactory):
	
	protocol = GameProtocol
	clients = {}			# maps client id to its protocol
	client_waiting = None	# id of client waiting for a partner to join
	game = None				# class of game to create every two connections
	next_id = 1				# id to give next client connection

	def __init__(self, game):
		self.game = game

	def buildProtocol(self, address):
		proto = ServerFactory.buildProtocol(self, address)
		self.clients[self.next_id] = proto
		if self.client_waiting is None:
			self.client_waiting = self.next_id
		else:
			self.game(self.client_waiting, self.next_id)
			self.client_waiting = None
		self.next_id += 1
		return proto

	def get_move_from(self, d, cid, game_state):
		self.clients[cid].prompt_for_move(game_state, d)

	def game_over(self, cid_win, cid_lose, draw, game_state):
		self.clients[cid_win].game_over(None if draw else True, game_state)
		self.clients[cid_lose].game_over(None if draw else False, game_state)
		del self.clients[cid_win]
		del self.clients[cid_lose]


factory = None


### API defined below. Game should call these functions ###

def get_move_from(cid, game_state):
	print 'Get from player', cid
	d = defer.Deferred()
	reactor.callWhenRunning(factory.get_move_from, d, cid, game_state)
	return d


def game_over(winner, loser, draw, game_state):
	factory.game_over(winner, loser, draw, game_state)


def run(game):
	""" An object of class 'game' is created for every two clients. """

	port = 8040
	iface = 'localhost'

	global factory
	factory = GameFactory(game)

	reactor.listenTCP(port, factory, interface=iface)
	reactor.run()



### Game stuff defined below. Move to separate module if necessary ###

class TicTacToe():
	
	def __init__(self, cid1, cid2):
		self.cid = {1: cid1, 2: cid2}
		self.state = [0,0,0,0,0,0,0,0,0]
		self.active = 1
		self._get_next_move()

	
	def move_received(self, move):
		print 'received:', move
		self.state[move] = self.active
		print 'new state:', self.state
		winner = self._winner(move)
		if winner == 0:
			self.active = 3 - self.active
			self._get_next_move()
		elif winner == -1:
			game_over(self.cid[1], self.cid[2], True, self.state)
		else:
			game_over(self.cid[winner], self.cid[3-winner], False, self.state)
			

	def err_received(self):
		raise Exception('Errback called')

	
	def _get_next_move(self):
		d = get_move_from(self.cid[self.active], self.state)
		d.addCallbacks(self.move_received, self.err_received)

	
	def _winner(self, move):
		# Check verticals
		if self.state[move] == self.state[move-3] == self.state[move-6]:
			return self.state[move]
		# Check horizontals
		row = 3 * (move / 3)
		if self.state[row] == self.state[row+1] == self.state[row+2]:
			return self.state[row]
		# Check diagonals
		if self.state[0] == self.state[4] == self.state[8] or \
			self.state[2] == self.state[4] == self.state[6]:
			return self.state[4]
		# Check draw
		if not 0 in self.state:
			return -1
		# No winner
		return 0



### Main External Call ###

if __name__ == '__main__':
	run(TicTacToe)