--Table structure for User

CREATE TABLE IF NOT EXISTS "user"(
	v_id varchar(64), 
	v_username varchar(64) PRIMARY KEY, 
	v_email varchar(64) CHECK (v_email LIKE '%@%'), 
	v_display_name varchar(64),
	v_access_token varchar(255),
	v_refresh_token varchar(255),
	v_auth_date timestamp,
	password char(40),
	password_salt char(25),
	last_pull_date timestamp NULL
);