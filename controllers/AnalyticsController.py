from model.database.table_managers.AnalyticsManager import AnalyticsManager
from model.database.table_managers.UserManager import UserManager
import os, requests, time, datetime, sys

class AnalyticsController:
	def __init__(self):
		self.AnalyticsManager = AnalyticsManager()
		self.username = None
		self.UserManager = UserManager()
		self.beforeDate = None

	def setUsername(self, username):
		self.username = username

	def getUsername(self):
		return self.username

	# update analytics for a user
	def updateAnalytics(self):
		if self.username == None:
			raise Exception('Missing Username')
		rawData = self.pullData()
		cleanData = self.refineData(rawData)
		self.insertData(cleanData)

	# pull data from venmo servers
	def pullData(self):
		try:
			v_access_token = self.returnOrRefreshTokens()
			if v_access_token:

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
				
				lastPullDate = self.UserManager.getLastPullDate(self.username)
				if len(lastPullDate) and lastPullDate[0][0] != None:
					# not the first time we are getting data so we need an after
					data['after'] = lastPullDate[0][0]

				# get data from venmo server
				response = requests.get(url, params=data)
				response_dict = response.json()
				if 'error' in response_dict:	
					e_str = "VenmoPullDataError: %s" % (response_dict['error']['message'],)
					raise Exception(e_str)

				# update before date in db
				# return venmo data
				else:
					self.UserManager.updateLastPullDate(before, self.username)
					return response_dict['data']
			else:
				raise Exception('Venmo Access Tokens not found')
		except:
			raise

	# get user tokens or refresh them
	def returnOrRefreshTokens(self,):

		try:
			result = self.UserManager.getUserTokens(self.username)
			if len(result):

				authDate = result[0][2]
				authEpoch = time.mktime(authDate.timetuple())
				currEpoch = time.time()
				if currEpoch - authEpoch > 0:
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

					# use a post for security purposes 
					response = requests.post(url,data)
					response_dict = response.json()
					if 'error' in response_dict:
						e_str = "VenmoAuthenticationError: %s" % (response_dict['error']['message'],)
						raise Exception(e_str)
						
					v_access_token = response_dict['access_token']
					v_refresh_token = response_dict['refresh_token']
					v_auth_date = time.strftime("%Y-%m-%d %H:%M:%S")

					# update the database
					self.UserManger.updateUserTokens(v_access_token,v_refresh_token,v_auth_date,self.username)
					return v_access_token
		except:
			raise

	# clean up data
	def refineData(self,rawData):
		cleanData = {}
		# traverse data
		try:
			for transaction in rawData:
				if transaction['status'] == 'settled':
					dayOfTrans = transaction['date_completed']
					tIndex = dayOfTrans.find('T')
					dayOfTrans = dayOfTrans[0:tIndex]
					
					# do a simple test to see if key is in dict
					# if not then we create the key
					try:
						cleanData[dayOfTrans]['user_name'] = self.username
					except KeyError:
						cleanData[dayOfTrans] = {'user_name':self.username,
												'num_trans_inflow':0,
												'num_trans_outflow':0,
												'inflow':0.0,
												'outflow':0.0,
												'largest_payment':0.0,
												'largest_charge':0.0,
												'ave_trans_size':0.0, # (inflow + outflow)/(num inflow + num outflow)
												'day_of_transactions':dayOfTrans
												}

					action = transaction['action']
					actor = transaction['actor']['username']
					# outflow
					if (actor == self.username and action == 'pay') or (actor != self.username and action == 'charge'):
						cleanData[dayOfTrans]['num_trans_outflow'] +=1
						cleanData[dayOfTrans]['outflow'] += transaction['amount']

					# inflow
					elif (actor == self.username and action == 'charge') or (actor != self.username and action == 'pay'):
						cleanData[dayOfTrans]['num_trans_inflow'] +=1
						cleanData[dayOfTrans]['inflow'] += transaction['amount']
					
					# largest
					if action == 'pay':
						cleanData[dayOfTrans]['largest_payment'] = max(cleanData[dayOfTrans]['largest_payment'], transaction['amount'])
					elif action == 'charge':
						cleanData[dayOfTrans]['largest_charge'] = max(cleanData[dayOfTrans]['largest_charge'], transaction['amount'])

					# ave trans amount	
					cleanData[dayOfTrans]['ave_trans_size'] = (cleanData[dayOfTrans]['inflow'] + cleanData[dayOfTrans]['outflow']) / (cleanData[dayOfTrans]['num_trans_inflow'] + cleanData[dayOfTrans]['num_trans_outflow'])
			return cleanData
		except:
			raise

	# insert data into database
	def insertData(self, cleanData):
		try:
			data_tuple = tuple(cleanData.values())
			self.AnalyticsManager.insertAnalytics(data_tuple)
		except:
			raise
	
	# send data to the view
	def retrieveAnalytics(self,):
		result = self.AnalyticsManager.retrieveAnalytics(self.username)
		return result
