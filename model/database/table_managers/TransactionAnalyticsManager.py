# Wrapper class for Transactions table table
from model.datastore.PostgresSQL import PostgresSQL

class TransactionAnalyticsManager:
	# __user_name 		   			= "user_name"
	# __num_trans_inflow		   	= "num_payments"
	# __num_trans_outflow		   	= "num_charges"
	# __inflow 						= "inflow"
	# __outflow  					= "outflow"
	#								= "largest_payment"
	#								= "largest_charge"
	#								= "ave_trans_size"
	#								= "day_of_transactions"
	# __date_pulled 				= "date_pulled"

	def __init__(self):
		self.PostgresSQL = PostgresSQL()

	def insertTransactions(self, vals):
		query = """INSERT INTO "transaction_analytics" VALUES \
		(%(user_name)s, %(num_trans_inflow)s, %(num_trans_outflow)s, %(inflow)s,\
		%(outflow)s, %(largest_payment)s, %(largest_charge)s, %(ave_trans_size)s,\
		%(day_of_transactions)s, %(date_pulled)s);"""

		self.PostgresSQL.insertMany(query, vals) 

	def getLastPullDate(self,user_name):
		query = """SELECT date_pulled from "transaction_analytics" where user_name=%s order by date_pulled desc limit 1;"""
		vals = (user_name,)
		
		return self.PostgresSQL.read(query,vals)

	def retrieveAnalytics(self, user_name):
		query = """SELECT Extract(YEAR FROM day_of_transactions) as year,\
				 	Extract(MONTH FROM day_of_transactions) as month,\
					SUM(outflow) as outflow, SUM(inflow) as inflow, SUM(num_trans_outflow) as qOutflow,\
					SUM(num_trans_inflow) as qInflow from transaction_analytics where user_name=%s group by year, month order by year, month;""" 

		vals =(user_name,)

		result = self.PostgresSQL.read(query, vals)
		return self.PostgresSQL.makeDataDict(result, ('Year','Month','outflow','inflow','qOutflow','qInflow'))
