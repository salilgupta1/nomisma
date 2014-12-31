-- Table structure for Analytics

CREATE TABLE IF NOT EXISTS "analytics"(
	user_name varchar(64) REFERENCES "user"(v_username)
		ON DELETE CASCADE,
	num_trans_inflow INT NOT NULL,
	num_trans_outflow INT NOT NULL, 
	inflow NUMERIC NOT NULL, 
	outflow NUMERIC NOT NULL, 
	largest_payment NUMERIC NOT NULL,
	largest_charge NUMERIC NOT NULL,
	ave_trans_size NUMERIC NOT NULL,
	day_of_transactions timestamp NOT NULL,

	CONSTRAINT day_user unique(user_name,day_of_transactions)
);