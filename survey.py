import sqlite3 as sq

class Survey:
	def __init__(self):
		self.con = sq.connect('survey.sqlite')
		self.cur = self.con.cursor()


	def drop_table(self):
		cmd = """
		DROP TABLE IF EXISTS Survey
		"""
		self.cur.execute(cmd)

	def set_table(self):
		cmd = """
		CREATE TABLE Survey(
		Content TEXT,
		User TEXT PRIMARY KEY NOT NULL,
		Response TEXT
		);
		"""
		self.cur.execute(cmd)

	def set_content(self, content):
		cmd = """
		INSERT INTO Survey(Content, User, Response)
		Values(?,?,?)
		"""
		self.cur.execute(cmd, (content, '-',''))
		self.con.commit()

	def add_entry(self, content, user):
		cmd = """
		SELECT EXISTS(SELECT 1 FROM Survey WHERE User=? COLLATE NOCASE) LIMIT 1
		"""
		found = self.cur.execute(cmd, (user,))

		if found.fetchone()[0] == 0:
			cmd = """
			INSERT INTO Survey(Content, User, Response)
			Values(?,?,?)
			"""
			self.cur.execute(cmd, ('',user,content))
		else:
			cmd = """
			UPDATE Survey SET Response = ? WHERE User = ?
			"""
			self.cur.execute(cmd, (content,user))
			
		self.con.commit()


	def get_survey(self):
		survey = ''
		
		cmd = """
		SELECT Content FROM Survey WHERE User = '-'
		"""

		survey += self.cur.execute(cmd).fetchone()[0]

		if survey != '':
			return survey
		return 'Error'

	def get_responses(self):
		cmd = """
		SELECT User,Response FROM Survey WHERE User != '-'
		"""
		self.cur.execute(cmd)
		return self.cur.fetchall()




