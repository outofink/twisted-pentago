#!c:/Python27/python.exe -u
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
import json
from os import system, name

class GameClientProtocol(Protocol):

	def dataReceived(self, data):
		msg = json.loads(data)
		
		if 'type' not in msg:
			print '[Error] Received invalid message from server'
		
		elif msg['type'] == 'prompt' and msg['value'] == 'move':
			print '[Server] Your turn to move!'
			m = self._get_move(msg['state'], msg['player'])
			self._send_move(m)

		elif msg['type'] == 'prompt' and msg['value'] == 'rotate':
			print '[Server] Your turn to rotate!'
			m = self._get_rotate(msg['state'], msg['player'])
			self._send_rotate(m)

		elif msg['type'] == 'prompt' and msg['value'] == 'shown':
			print '[Server] Your turn to show!'
			m = self._get_shown(msg['state'], msg['player'])
			self._send_shown(m)

		elif msg['type'] == 'prompt' and msg['value'] == 'init':
			print '[Server] Your turn to init!'
			m = self._get_init(msg['state'], msg['player'])
			self._send_init(m)

		elif msg['type'] == 'winner':
			system('cls' if name == 'nt' else 'clear')
			if  msg['player'] % 2 == 1:
				pcolor = "White"
			else:
				pcolor = "Black"
			print "You are %s:\n" % pcolor.upper()
			self._print_board(msg['state'])
			if msg['value'] == None:
				print 'You tied!'
			elif msg['value'] == True:
				print 'You won!'
			else:
				print 'You lost!'
			self.transport.loseConnection()
			#reactor.stop()

		elif msg['type'] == 'error':
			print '[Server] {}'.format(msg['value'])
		
		else:
			print '[Server:{}] {}'.format(msg['type'], msg['value'])

	
	def _get_move(self, state, player):
		move = None
		pass3 = False
		while pass3 == False or state[move] != 0:
			system('cls' if name == 'nt' else 'clear')
			if player % 2 == 1:
				pcolor = "White"
			else:
				pcolor = "Black"
			print "You are %s:\n" % pcolor.upper()
			self._print_board(state)
			pass0 = False
			pass1 = False
			pass2 = False
			pass3 = False
			rawloc=raw_input("Location (ie. A4 or C9): ")
			rawloc=rawloc.strip()
			if (len(rawloc)) == 2:
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
				pass3=True
				place=int(rawloc[-1])-1
				move = place + (9 * square)
		if player == 1:
			color = 1
		else:
			color = 2
		state[move]=color
		system('cls' if name == 'nt' else 'clear')
				
		return move

	def rotateCC(self, board, sector):
		nboard=[[" "]*9]*4
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
		nboard=[[" "]*9]*4
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

	def boardToState(self, board):
		state = board[0] + board[1] + board[2] + board[3]
		return state

	def _get_rotate(self, state, player):
		pstate=[state[:9], state[9:18], state[18:27], state[27:36]]
		pass3 = False
		while pass3 == False:
			system('cls' if name == 'nt' else 'clear')
			if player % 2 == 1:
				pcolor = "White"
			else:
				pcolor = "Black"
			print "You are %s:\n" % pcolor.upper()
			self._print_board(state)
			pass0 = False
			pass1 = False
			pass2 = False
			rawrot=raw_input("Rotation (ie. A' or C\"): ")
			rawrot = rawrot.strip()
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
					rotate = self.rotateC(pstate, square)
				else:
					rotate = self.rotateCC(pstate, square)
				print rotate
				print
				rotate = self.boardToState(rotate)
				print rotate
				pass3 = True

		if player % 2 == 1:
			tcolor = "Black" #opposite color
			pcolor = "White"
		else:
			tcolor = "White" #opposite color
			pcolor = "Black"

		state=rotate

		system('cls' if name == 'nt' else 'clear')
		print "You are %s:\n" % pcolor.upper()
		self._print_board(state)
		print "Waiting for %s to move..." % tcolor
		return rotate

	def _get_shown(self, state, player):
		if player % 2 == 1:
			tcolor = "Black" #opposite color
			pcolor = "White"
		else:
			tcolor = "White" #opposite color
			pcolor = "Black"
		system('cls' if name == 'nt' else 'clear')
		print "You are %s:\n" % pcolor.upper() 
		self._print_board(state)
		print "Waiting for %s to rotate..." % tcolor
		return True

	def _get_init(self, state, player):
		system('cls' if name == 'nt' else 'clear')
		print "You are WHITE:\n"
		self._print_board(state)
		print "Waiting for Black to move..."
		return True

	def _send_move(self, move):
		data_out = dict(type="move", value=move)
		self.transport.write(json.dumps(data_out))

	def _send_rotate(self, rotate):
		data_out = dict(type="rotate", value=rotate)
		self.transport.write(json.dumps(data_out))

	def _send_shown(self, shown):
		data_out = dict(type="shown", value=shown)
		self.transport.write(json.dumps(data_out))

	def _send_init(self, init):
		data_out = dict(type="init", value=init)
		self.transport.write(json.dumps(data_out))

	def _print_board(self, state):
		y=0
		dstate= list(state)
		for x in state:
			if x == 1:
				dstate[y]="W"
			elif x == 2:
				dstate[y]="B"
			else:
				dstate[y]=" "
			y+=1
		f = lambda x: ' ' if x == 0 else x
		pstate=[dstate[:9], dstate[9:18], dstate[18:27], dstate[27:36]]
		print """\
	{0[0][0]} {0[0][1]} {0[0][2]}|{0[1][0]} {0[1][1]} {0[1][2]}
	{0[0][3]} {0[0][4]} {0[0][5]}|{0[1][3]} {0[1][4]} {0[1][5]}
	{0[0][6]} {0[0][7]} {0[0][8]}|{0[1][6]} {0[1][7]} {0[1][8]}
	-----+-----
	{0[2][0]} {0[2][1]} {0[2][2]}|{0[3][0]} {0[3][1]} {0[3][2]}
	{0[2][3]} {0[2][4]} {0[2][5]}|{0[3][3]} {0[3][4]} {0[3][5]}
	{0[2][6]} {0[2][7]} {0[2][8]}|{0[3][6]} {0[3][7]} {0[3][8]}\n""".format(pstate)

	def connectionMade(self):
		print "You are WHITE:\n"
		self._print_board([" "]*36)
		print "Waiting for Black to connect..."


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