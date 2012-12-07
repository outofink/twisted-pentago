import sqlite3

conn = sqlite3.connect('tictactoe.db')
c = conn.cursor()

### DDL goes here ###

create_statements = '''
CREATE TABLE IF NOT EXISTS games (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	cid1 INTEGER NOT NULL,
	cid2 INTEGER NOT NULL,
	p0 INTEGER NOT NULL,
	p1 INTEGER NOT NULL,
	p2 INTEGER NOT NULL,
	p3 INTEGER NOT NULL,
	p4 INTEGER NOT NULL,
	p5 INTEGER NOT NULL,
	p6 INTEGER NOT NULL,
	p7 INTEGER NOT NULL,
	p8 INTEGER NOT NULL,
	done BOOLEAN NOT NULL,
	winner INTEGER NOT NULL ) '''

c.execute(create_statements)


### API goes here ###

def create_game(cid1, cid2):
	dml = ''' INSERT INTO games(cid1, cid2, p0, p1, p2, p3, p4, p5, p6, p7, p8, done, winner)
			  VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) '''
	c.execute(dml, (cid1, cid2))
	conn.commit()


def make_move(cid, player, move):
	colc = 'cid' + str(player)	# This might be prone to SQL injections
	colm = 'p' + str(move)	# This might be prone to SQL injections
	dml = 'UPDATE games SET {}=? WHERE done=0 AND {}=?'.format(colm, colc)
	c.execute(dml, (player, cid))
	conn.commit()


def game_over(cid, player, draw):
	colc = 'cid' + str(player)	# This might be prone to SQL injections
	winner = 0 if draw else player
	dml = 'UPDATE games SET done=1, winner=? WHERE done=0 and {}=?'.format(colc)
	c.execute(dml, (winner, cid))
	conn.commit()


def get_state(cid, done=False):
	q = '''SELECT p0, p1, p2, p3, p4, p5, p6, p7, p8 
		   FROM games
		   WHERE done=? AND (cid1=? OR cid2=?)  '''
	c.execute(q, (done, cid, cid))
	return c.fetchone()


def count_derived(state):
	# Searches for completed games that can be derived from a particular state
	# Returns a tuple (a, b, c) where:
	# 	a is the number of such games that resulted in a draw
	# 	b is the number of such games won by player 1
	# 	c is the number of such games won by player 2
	stmts = ['done=1'] + ['p{}={}'.format(i, state[i]) for i in xrange(9) if state[i] != 0] # This might be prone to SQL injections
	where = ' AND '.join(stmts)	
	q = ''' SELECT winner, count(*)
			FROM games
			WHERE {}
			GROUP BY winner '''.format(where)
	c.execute(q)
	result = c.fetchall()
	r = [0, 0, 0]
	for a, b in result:
		r[a] = b
	return tuple(r)