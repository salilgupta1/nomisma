import psycopg2 as psql
import sys, os, re

class PostgresSQL():
	# pseudo private static vars
	__DBUSER = "" 
	__DBPWD  = ""
	__DBHOST = ""
	__DBPORT = 0
	__DBNAME = ""

	def __init__(self):
		db_url = os.environ['DATABASE_URL']
		parameters = re.split('@|:|\/\/|\/',db_url)[2:]
		PostgresSQL.__DBUSER = parameters[0]
		PostgresSQL.__DBPWD = parameters[1]
		PostgresSQL.__DBHOST = parameters[2]
		PostgresSQL.__DBPORT = parameters[3]
		PostgresSQL.__DBNAME = parameters[4]	

	def makeConn(self):
		try:
			conn = psql.connect(database=PostgresSQL.__DBNAME,
								user=PostgresSQL.__DBUSER,
								password=PostgresSQL.__DBPWD,
								host=PostgresSQL.__DBHOST,
								port=PostgresSQL.__DBPORT)
			return conn
		except:
			raise

	def makeDataDict(self, results, columns):
		try:
			obj = {"results":[]}	
			for row in results:
				obj['results'].append(dict(zip(columns, row)))
			return obj
		except:
			raise

	def read(self, query, vals):
		try:
			conn = self.makeConn()
			cur = conn.cursor()
			cur.execute(query,vals)
			rows = cur.fetchall()
			conn.close()
			return rows
		except:
			raise

	def insert(self, query, vals):
		try:
			conn = self.makeConn()
			curr = conn.cursor()
			curr.execute(query,vals)
			conn.commit()
			conn.close()
		except:
			raise

	def insertMany(self, query, vals):
		try:
			conn = self.makeConn()
			curr = conn.cursor()
			curr.executemany(query, vals)
			conn.commit()
			conn.close()
		except:
			raise

	def update(self, query, vals):
		try:
			conn = self.makeConn()
			curr = conn.cursor()
			curr.execute(query,vals)
			conn.commit()
			conn.close()
		except:
			raise
