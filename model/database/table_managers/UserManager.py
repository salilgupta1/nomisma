# Wrapper class for User table
from model.datastore.PostgresSQL import PostgresSQL

class UserManager:
	# __v_id		   		= "v_id"
	# __v_username   		= "v_username"
	# __v_email	   			= "v_email"
	# __v_display_name		= "v_display_name"
	# __v_access_token  	= "v_access_token"
	# __v_refresh_token 	= "v_refresh_token"
	# __v_auth_date			= "v_auth_date"
	# __password 			= "password"
	# __password_salt		= "password_salt"
	# __last_pull_date		= "last_pull_date"

	def __init__(self):
		self.PostgresSQL = PostgresSQL()

	def createUser(self,vals):
		# insert a user into the db
		
		query = """INSERT INTO "user" VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
		self.PostgresSQL.insert(query,vals)
		
	def getUserTokens(self,v_user_name):
		# get the user authentication tokens
		
		query = """SELECT v_access_token, v_refresh_token, v_auth_date from "user" where v_username = %s;"""
		vals = (v_user_name,)
		
		return self.PostgresSQL.read(query,vals)

	def updateUserTokens(self,accessToken,refreshToken, authDate,v_user_name):
		# update a users authentication tokens
		
		query = """UPDATE "user" SET v_access_token=%s, v_refresh_token=%s, v_auth_date=%s where v_username=%s;"""
		vals = (accessToken,refreshToken,authDate,v_username)

		self.PostgresSQL.update(query,vals)

	def getUserAuth(self, username):
		# get user auth for login
		
		query = """SELECT password, password_salt from "user" where v_username=%s;"""
		vals = (username,)

		return self.PostgresSQL.read(query,vals)

	def getLastPullDate(self,username):
		query = """SELECT last_pull_date from "user" where v_username=%s;"""
		vals = (username,)
		
		return self.PostgresSQL.read(query,vals)

	def updateLastPullDate(self, new_pull_date, username):
		query = """UPDATE "user" SET last_pull_date=%s where v_username=%s;"""
		vals = (new_pull_date,username)

		self.PostgresSQL.update(query,vals)