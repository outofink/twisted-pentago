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
		#if a move was done 
		elif msg['type'] == 'move':
			if self.active:
				self.deferred.callback( msg['value'] )
			else:
				self._send_error('Not your turn yet')
		elif msg['type'] == 'rotate':
			if self.active:
				self.deferred.callback( msg['value'] )
				self.deferred = None
				self.active = False
			else:
				self._send_error('Not your turn yet')
		else:
			self._send_error('Received unknown message type')

	def prompt_for_move(self, game_state, d, cid):
		self.active = True
		self.deferred = d
		data_out = dict(type='prompt', value='move', state=game_state, player=cid)
		self.transport.write(json.dumps(data_out))

	def prompt_for_rotate(self, game_state, d, cid):
		self.active = True
		self.deferred = d
		data_out = dict(type='prompt', value='rotate', state=game_state, player=cid)
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
                #goes and asks client for a move
		self.clients[cid].prompt_for_move(game_state, d, cid)

	def get_rotate_from(self, d, cid, game_state):
                #goes and asks client for a move
		self.clients[cid].prompt_for_rotate(game_state, d, cid)

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

def get_rotate_from(cid, game_state):
	print 'Get from player', cid
	d = defer.Deferred()
	reactor.callWhenRunning(factory.get_rotate_from, d, cid, game_state)
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
