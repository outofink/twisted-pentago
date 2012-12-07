from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
import json
from gamedb import count_derived
from random import choice as random_choice


class GameClientProtocol(Protocol):
	
	def dataReceived(self, data):
		msg = json.loads(data)
		
		if 'type' not in msg:
			print '[Error] Received invalid message from server'
		
		elif msg['type'] == 'prompt' and msg['value'] == 'move':
			m = self._get_move(msg['state'])
			print '[AI] Sending move:', m
			self._send_move(m)

		elif msg['type'] == 'winner':
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
		statel = list(state)
		me = 1 if state.count(1) == state.count(2) else 2
		best_score, best_move = None, None
		for i in xrange(9):
			if state[i] == 0:
				# Get stats for potential move
				statel[i] = me
				draws, p1wins, p2wins = count_derived(statel)
				statel[i] = 0
				# Heuristic score for that move
				score = p1wins - p2wins if me == 1 else p2wins - p1wins
				try:
					score = float(score) / (draws + p1wins + p2wins)
				except ZeroDivisionError:
					score = 0
				# Compare score against previous best
				if score > best_score:
					best_score, best_move = score, [i]
				elif score == best_score:
					best_move.append(i)
		return random_choice(best_move)


	def _send_move(self, move):
		data_out = dict(type="move", value=move)
		self.transport.write(json.dumps(data_out))


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