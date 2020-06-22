import sqlite3

conn = sqlite3.connect('pentago.db')
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
	p9 INTEGER NOT NULL,
	p10 INTEGER NOT NULL,
	p11 INTEGER NOT NULL,
	p12 INTEGER NOT NULL,
	p13 INTEGER NOT NULL,
	p14 INTEGER NOT NULL,
	p15 INTEGER NOT NULL,
	p16 INTEGER NOT NULL,
	p17 INTEGER NOT NULL,
	p18 INTEGER NOT NULL,
	p19 INTEGER NOT NULL,
	p20 INTEGER NOT NULL,
	p21 INTEGER NOT NULL,
	p22 INTEGER NOT NULL,
	p23 INTEGER NOT NULL,
	p24 INTEGER NOT NULL,
	p25 INTEGER NOT NULL,
	p26 INTEGER NOT NULL,
	p27 INTEGER NOT NULL,
	p28 INTEGER NOT NULL,
	p29 INTEGER NOT NULL,
	p30 INTEGER NOT NULL,
	p31 INTEGER NOT NULL,
	p32 INTEGER NOT NULL,
	p33 INTEGER NOT NULL,
	p34 INTEGER NOT NULL,
	p35 INTEGER NOT NULL,
	done BOOLEAN NOT NULL,
	winner INTEGER NOT NULL ) '''

c.execute(create_statements)


### API goes here ###

def create_game(cid1, cid2):
	dml = ''' INSERT INTO games(cid1, cid2, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35, done, winner)
			  VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) '''
	c.execute(dml, (cid1, cid2))
	conn.commit()


def make_move(cid, player, move):
	colc = 'cid' + str(player)	# This might be prone to SQL injections
	colm = 'p' + str(move)	# This might be prone to SQL injections
	dml = 'UPDATE games SET {}=? WHERE done=0 AND {}=?'.format(colm, colc)
	c.execute(dml, (player, cid))
	conn.commit()

def make_rotate(cid, player, rotate):
	# values = ', '.join(str(e) for e in rotate)
	colc = 'cid' + str(player)	# This might be prone to SQL injections

	for x in range(36):
		colm = 'p' + str(x)	# This might be prone to SQL injections
		dml = 'UPDATE games SET {}=? WHERE done=0 AND {}=?'.format(colm, colc)
		c.execute(dml, (rotate[x], cid))
	conn.commit()

def game_over(cid, player, draw):
	colc = 'cid' + str(player)	# This might be prone to SQL injections
	winner = 0 if draw else player
	dml = 'UPDATE games SET done=1, winner=? WHERE done=0 and {}=?'.format(colc)
	c.execute(dml, (winner, cid))
	conn.commit()


def get_state(cid, done=False):
	q = '''SELECT p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35
		   FROM games
		   WHERE done=? AND (cid1=? OR cid2=?)  '''
	c.execute(q, (done, cid, cid))
	return c.fetchone()
