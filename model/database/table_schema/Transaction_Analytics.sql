-- Table structure for Transaction Analytics

CREATE TABLE IF NOT EXISTS "transaction_analytics"(
	user_name varchar(64) REFERENCES "user"(v_username)
		ON DELETE CASCADE,
	num_payments INT NOT NULL,
	num_charges INT NOT NULL, 
	ave_bal NUMERIC NOT NULL, 
	amt_payments NUMERIC NOT NULL, 
	amt_charges NUMERIC NOT NULL, 
	most_paid_friend varchar(64) NOT NULL, 
	most_charged_friend varchar(64) NOT NULL, 
	date_pulled timestamp NOT NULL,

	CONSTRAINT date_pulled_unique_for_transaction unique(user_name,date_pulled)
);