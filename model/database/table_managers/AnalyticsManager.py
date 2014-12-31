# Wrapper class for Analytics table
from model.datastore.PostgresSQL import PostgresSQL

class AnalyticsManager:
	# __user_name 		   			= "user_name"
	# __num_trans_inflow		   	= "num_payments"
	# __num_trans_outflow		   	= "num_charges"
	# __inflow 						= "inflow"
	# __outflow  					= "outflow"
	#								= "largest_payment"
	#								= "largest_charge"
	#								= "ave_trans_size"
	#								= "day_of_transactions"

	def __init__(self):
		self.PostgresSQL = PostgresSQL()

	def insertAnalytics(self, vals):
		query = """INSERT INTO "analytics" VALUES \
		(%(user_name)s, %(num_trans_inflow)s, %(num_trans_outflow)s, %(inflow)s,\
		%(outflow)s, %(largest_payment)s, %(largest_charge)s, %(ave_trans_size)s,\
		%(day_of_transactions)s);"""

		self.PostgresSQL.insertMany(query, vals) 

	def getCharts(self, user_name):
		query = """SELECT Extract(YEAR FROM day_of_transactions) as year,\
				 	Extract(MONTH FROM day_of_transactions) as month,\
					SUM(outflow) as outflow, SUM(inflow) as inflow, SUM(num_trans_outflow) as qOutflow,\
					SUM(num_trans_inflow) as qInflow from analytics where user_name=%s group by year, month order by year, month;""" 

		vals =(user_name,)

		result = self.PostgresSQL.read(query, vals)
		return self.PostgresSQL.makeDataDict(result, ('Year','Month','outflow','inflow','qOutflow','qInflow'))

	def getStandAlones(self, user_name):
		query = """SELECT ROUND(avg(inflow),2) as aveInflow, ROUND(avg(outflow),2) as aveOutflow, sum(inflow) - sum(outflow) as net  FROM analytics where user_name=%s;"""
		vals =(user_name,)
		result = self.PostgresSQL.read(query, vals)
		return self.PostgresSQL.makeDataDict(result, ('aveInflow','aveOutflow','net'))
