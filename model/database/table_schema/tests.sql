
-- delete users should on cascade
delete from "user";

--should return 0 rows deleted
delete from "transaction_analytics";

-- insert into User
-- should pass
insert into "user" ("v_id","v_username", "v_email", "v_first_name","v_last_name") values ('23','salilgupta1','salil@uniplus.com','salil','gupta');

-- should fail, bad email
insert into "user" ("v_id","v_username", "v_email", "v_first_name","v_last_name") values ('23','salilgupta1','saliluniplus.com','salil','gupta');


--insert into transaction_analytics
-- should pass
--insert into "transaction_analytics" ("u_id","num_payments","num_charges","ave_bal","amt_payments","amt_charges","most_paid_friend","most_charged_friend","date_pulled") values (4,40,50,51.40,370.00,200.00,'Sanjeet','Sanjeet', "2013-12-30T19:40:57");

-- should fail
-- ref integrity
--insert into "transaction_analytics" ("u_id","num_payments","num_charges","ave_bal","amt_payments","amt_charges","most_paid_friend","most_charged_friend","date_pulled") values (1000,40,50,51.40,370.00,200.00,'Sanjeet','Sanjeet', "2014-12-30T19:40:57");

-- should fail
-- unique constraint error
--insert into "transaction_analytics" ("u_id","num_payments","num_charges","ave_bal","amt_payments","amt_charges","most_paid_friend","most_charged_friend","date_pulled") values (4,40,50,51.40,370.00,200.00,'Sanjeet','Sanjeet', "2013-12-30T19:40:57");
