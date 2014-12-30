from model.database.table_managers.UserManager import UserManager
import os, requests, hashlib, time

class UserAuthController():

	def __init__(self):
		self.UserManager = UserManager()
		self.regData = None

	def authenticateUser(self,username, password):

		result = self.UserManager.getUserAuth(username)
		if len(result) > 0:
			db_password = result[0][0]
			db_salt = result[0][1]
			password = password + db_salt
			hashed = hashlib.sha1(password).hexdigest()
			if (hashed == db_password):
				return True
		return "Oops! Invalid Username or Password...."

	def authorizeWithVenmo(self,code):
		try:
			data = {
				"client_id":os.environ['client_id'],
				"client_secret":os.environ['client_secret'], 
				"code":code
			}

			url = "https://api.venmo.com/v1/oauth/access_token"

			# do the actual retrieval of user information
			response = requests.post(url, data)
			response_dict = response.json()

			if 'error' in response_dict:
				# raise a venmo exception
				e_str = "VenmoAuthenticationError: %s" % (response_dict['error']['message'],)
				raise Exception(e_str)
			else:
				v_id = response_dict['user']['id']
				v_user_name = response_dict['user']['username']
				v_email = response_dict['user']['email']
				v_display_name = response_dict['user']['display_name']
				v_access_token = response_dict['access_token']
				v_refresh_token = response_dict['refresh_token']
				v_auth_date = time.strftime("%Y-%m-%d %H:%M:%S")
				self.regData = (v_id,v_user_name,v_email,v_display_name,v_access_token,v_refresh_token,v_auth_date)
				return v_user_name
		except:
			raise

	def completeRegistration(self,username,password):
		try:
			# create salt and encrypt password
			salt = os.urandom(16).encode('base-64')
			password += salt
			password = hashlib.sha1(password).hexdigest()
			self.regData +=(password,salt)
			
			# create the user
			self.UserManager.createUser(self.regData)
		except:
			raise
