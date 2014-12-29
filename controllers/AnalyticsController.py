from model.database.table_managers.TransactionAnalyticsManager import TransactionAnalyticsManager
from model.database.table_managers.UserManager import UserManager
import os, requests, time, datetime, sys

class AnalyticsController:
	def __init__(self):
		self.TransactionAnalyticsManager = TransactionAnalyticsManager()
		self.username = None
		self.UserManager = UserManager()
		self.rawData = {}
		self.cleanData = {}
		self.beforeDate = None

	def setUsername(self, username):
		self.username = username

	def updateVenmoAnalytics(self):
		pullError = self.pullData()
		if pullError == True:
			refineError= self.refineData()
			if refineError == True:
				insertError = self.insertData()
				if insertError == True:
					return True

		# some sort of error so send to index for now ..
		return "Error"

	# pull data from venmo servers
	def pullData(self):
		try:
			v_access_token = self.returnOrRefreshTokens()
			print v_access_token
			if v_access_token is not "Error":

				url = "https://api.venmo.com/v1/payments"

				# store this in the database 
				before = time.strftime("%Y-%m-%d")

				todayPlusOne = datetime.date.today() + datetime.timedelta(days=1)
				todayPlusOne = todayPlusOne.strftime("%Y-%m-%d")
				data = {
					"before":todayPlusOne,
					"limit":10000,
					"access_token":v_access_token
				}
				
				lastPullDate = self.TransactionAnalyticsManager.getLastPullDate(self.username)
				if len(lastPullDate):
					# not the first time we are getting data so we need an after
					data['after'] = lastPullDate[0][0]

				# get data from venmo server
				response = requests.get(url, params=data)
				response_dict = response.json()
				if 'error' in response_dict:
					
					# There was an error
					print response_dict['error']
					return "Error"

				# data plus before date to save in db later
				else:
					self.beforeDate = before
					self.rawData = response_dict['data']
					# no error
					return True
			else:
				# return an error
				return "Error"
		except:
			raise
			return "Error"

	# get user tokens or refresh them
	def returnOrRefreshTokens(self,):

		try:
			result = self.UserManager.getUserTokens(self.username)
			print result
			if result !='Error' and len(result):

				authDate = result[0][2]
				authEpoch = time.mktime(authDate.timetuple())
				currEpoch = time.time()
				print authEpoch
				if currEpoch - authEpoch > 0:
					print "hi"
					# no need to refresh just return access_token
					return result[0][0]
				else:	

					# we must refresh tokens
					data = {
		    			"client_id": os.environ['client_id'],
		    			"client_secret": os.environ['client_secret'],
		   				"refresh_token": result[0][1]
					}
					url = "https://api.venmo.com/v1/oauth/access_token"

					# use a post for security purposes ... 
					response = requests.post(url,data)
					response_dict = response.json()

					v_access_token = response_dict['access_token']
					v_refresh_token = response_dict['refresh_token']
					v_auth_date = time.strftime("%Y-%m-%d %H:%M:%S")

					# update the database
					updateResult = self.UserManger.updateUserTokens(v_access_token,v_refresh_token,v_auth_date,self.username)
					
					if updateResult !='Error':

						# if no error with db update return access_token
						return v_access_token
		except:
			raise
			return "Error"

	# clean up data
	def refineData(self,):

		# traverse data
		try:
			for transaction in self.rawData:
				if transaction['status'] == 'settled':
					dayOfTrans = transaction['date_completed']
					tIndex = dayOfTrans.find('T')
					dayOfTrans = dayOfTrans[0:tIndex]
					
					# do a simple test to see if key is in dict
					# if not then we create the key
					try:
						self.cleanData[dayOfTrans]['user_name'] = self.username
					except KeyError:
						self.cleanData[dayOfTrans] = {'user_name':self.username,
												'num_trans_inflow':0,
												'num_trans_outflow':0,
												'inflow':0.0,
												'outflow':0.0,
												'largest_payment':0.0,
												'largest_charge':0.0,
												'ave_trans_size':0.0, # (inflow + outflow)/(num inflow + num outflow)
												'date_pulled':self.beforeDate,
												'day_of_transactions':dayOfTrans
												}

					action = transaction['action']
					actor = transaction['actor']['username']
					# outflow
					if (actor == self.username and action == 'pay') or (actor != self.username and action == 'charge'):
						self.cleanData[dayOfTrans]['num_trans_outflow'] +=1
						self.cleanData[dayOfTrans]['outflow'] += transaction['amount']

					# inflow
					elif (actor == self.username and action == 'charge') or (actor != self.username and action == 'pay'):
						self.cleanData[dayOfTrans]['num_trans_inflow'] +=1
						self.cleanData[dayOfTrans]['inflow'] += transaction['amount']
					
					# largest
					if action == 'pay':
						self.cleanData[dayOfTrans]['largest_payment'] = max(self.cleanData[dayOfTrans]['largest_payment'], transaction['amount'])
					elif action == 'charge':
						self.cleanData[dayOfTrans]['largest_charge'] = max(self.cleanData[dayOfTrans]['largest_charge'], transaction['amount'])

					# ave trans amount	
					self.cleanData[dayOfTrans]['ave_trans_size'] = (self.cleanData[dayOfTrans]['inflow'] + self.cleanData[dayOfTrans]['outflow']) / (self.cleanData[dayOfTrans]['num_trans_inflow'] + self.cleanData[dayOfTrans]['num_trans_outflow'])
			return True
		except:
			raise
			return "Error"

	# insert data into database
	def insertData(self,):
		try:
			data_tuple = tuple(self.cleanData.values())
			result = self.TransactionAnalyticsManager.insertTransactions(data_tuple)
			return True
		except:
			raise
			return "Error"
	
	# send data for displaying
	def retrieveAnalytics(self,):
		result = self.TransactionAnalyticsManager.retrieveAnalytics(self.username)
		return result
