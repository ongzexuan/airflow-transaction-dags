CREATE TABLE transactions(
	transaction_id text PRIMARY KEY,
	pending_transaction_id text,
	account_id text NOT NULL, 
	name text NOT NULL,
	amount real NOT NULL,
	category_id integer,
	category text[],
	date date NOT NULL,
	iso_currency_code varchar(3),
	location json,
	payment_channel text,
	transaction_type text,
	pending boolean,
	payment_reference text,
	merchant text
)