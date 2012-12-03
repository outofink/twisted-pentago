from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import defer, reactor
import json

class GameProtocol(Protocol):

	play_id = 0
	active = False

	def dataReceived(self, data):
		msg = json.loads(data)
		if 'type' not in msg:
			self._send_error('Received improper message')
		elif msg['type'] == 'move':
			if self.active:
				self.factory.deferred.callback( msg['value'] )
				self.active = False
			else:
				self._send_error('Not your turn yet')
		else:
			self._send_error('Received unknown message type')

	def prompt_for_move(self, game_state):
		self.active = True
		data_out = dict(type='prompt', value='move', state=game_state)
		self.transport.write(json.dumps(data_out))

	def inform_winner(self, is_winner, game_state):
		data_out = dict(type='winner', value=is_winner, state=game_state)
		self.transport.write(json.dumps(data_out))
		self.transport.loseConnection()

	def _send_error(self, msg):
		data_out = dict(type='error', value=msg)
		self.transport.write(json.dumps(data_out))



class GameFactory(ServerFactory):
	
	protocol = GameProtocol
	play_id = 1
	clients = {}
	deferred = None	# send move to callback of this deferred

	def buildProtocol(self, address):
		proto = ServerFactory.buildProtocol(self, address)
		proto.play_id = self.play_id
		self.clients[self.play_id] = proto
		self.play_id += 1
		return proto

	def get_move_from(self, d, active, game_state):
		self.deferred = d
		if active in self.clients:
			self.clients[active].prompt_for_move(game_state)
		else:
			reactor.callLater(0.1, self.get_move_from, d, active, game_state)

	def inform_winner(self, winner, game_state):
		for client in self.clients:
			win_value = None if winner == -1 else winner == client #True/False/None
			self.clients[client].inform_winner(win_value, game_state)


factory = GameFactory()


### API defined below. Game should call these functions ###

def get_move_from(player, game_state):
	print 'Get from player', player
	d = defer.Deferred()
	reactor.callWhenRunning(factory.get_move_from, d, player, game_state)
	return d


def inform_winner(player, game_state):
	print 'Winner is', player
	factory.inform_winner(player, game_state)


def run(game):
	port = 8040
	iface = 'localhost'

	reactor.listenTCP(port, factory, interface=iface)
	get_move_from(game.active, game.state).addCallbacks(game.move_received, game.err_received)
	reactor.run()



### Game stuff defined below. Move to separate module if necessary ###

class TicTacToe():

	state = [0,0,0,0,0,0,0,0,0]
	active = 1

	def move_received(self, move):
		print 'received:', move
		self.state[move] = self.active
		print 'new state:', self.state
		winner = self._winner(move)
		if winner != 0:
			inform_winner(winner, self.state)
		else:
			self.active = 3 - self.active
			d = get_move_from(self.active, self.state)
			d.addCallbacks(self.move_received, self.err_received)


	def err_received(self):
		raise Exception('Errback called')


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
	run(TicTacToe())