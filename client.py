from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
import json


class GameClientProtocol(Protocol):
	
	def dataReceived(self, data):
		msg = json.loads(data)
		
		if 'type' not in msg:
			print '[Error] Received invalid message from server'
		
		elif msg['type'] == 'prompt' and msg['value'] == 'move':
			print '[Server] Your turn to move!'
			m = self._get_move(msg['state'])
			self._send_move(m)

		elif msg['type'] == 'winner':
			self._print_board(msg['state'])
			if msg['value'] == None:
				print '[Server] You have tied!'
			elif msg['value'] == True:
				print '[Server] You have won!'
			else:
				print '[Server] You have lost!'
			self.transport.loseConnection()
			reactor.stop()

		elif msg['type'] == 'error':
			print '[Server] {}'.format(msg['value'])
		
		else:
			print '[Server:{}] {}'.format(msg['type'], msg['value'])

	
	def _get_move(self, state):
		self._print_board(state)
		move = None
		while move is None or move < 0 or move > 8 or state[move] != 0:
			try:
				move = int(raw_input('Your move: '))
			except ValueError:
				move = None
		return move

	def _send_move(self, move):
		data_out = dict(type="move", value=move)
		self.transport.write(json.dumps(data_out))

	def _print_board(self, state):
		f = lambda x: ' ' if x == 0 else x
		print '------------|'
		print '| {} | {} | {} |'.format(*map(f, state[:3]))
		print '|-----------|'
		print '| {} | {} | {} |'.format(*map(f, state[3:6]))
		print '|-----------|'
		print '| {} | {} | {} |'.format(*map(f, state[6:]))
		print '|------------'


class GameClientFactory(ClientFactory):

	protocol = GameClientProtocol


### Main External Call ###

def main():
	host = 'localhost'
	port = 8040
	reactor.connectTCP(host, port, GameClientFactory())
	reactor.run()


if __name__ == '__main__':
	main()