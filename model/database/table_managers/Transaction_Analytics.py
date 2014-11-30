# Wrapper class for User table
from model.datastore.PostgresSQL import PostgresSQL

class Transaction_Analytics:
	# __user_name 		   	= "user_name"
	# __num_payments		   	= "num_payments"
	# __num_charges		   	= "num_charges"
	# __ave_bal	   			= "ave_bal"
	# __amt_payments 			= "amt_payments"
	# __amt_charges  			= "amt_charges"
	# __most_paid_friend 		= "most_paid_friend"
	# __most_charged_friend 	= "most_charged_friend"
	# __date_pulled 			= "date_pulled"


	def __init__(self):
		self.PostgresSQL = PostgresSQL()

	def saveWeekTransactionData(self,user_name,num_payments,num_charges,ave_bal,amt_payments,amt_charges,most_paid_friend,most_charged_friend,date_pulled):
		# save one weeks transaction data one at a time... 
		query = """INSERT INTO "transaction_analytics" VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
		vals = (user_name,num_payments,num_charges,ave_bal,amt_payments,amt_charges,most_paid_friend,most_charged_friend,date_pulled)

		print query
		result = self.PostgresSQL.insert(query,vals)
		return result

	def getTransactionData(self,startDate,endDate,user_name):
		# pull transaction data
		query = """SELECT num_payments,num_charges,ave_bal,amt_payments,amt_charges,most_paid_friend,most_charged_friend FROM "transaction_analytics" WHERE user_name = date_pulled and %s < %s and date_pulled > %s;"""
		vals = (user_name,startDate,endDate)
		
		print query
		result = self.PostgresSQL.read(query)
		return result
