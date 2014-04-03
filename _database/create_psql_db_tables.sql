-- create users psql database for Currency Converter Client
-- user already exists
-- must connect to db as follows: >psql -h localhost -p 5432 -U username db_name
DROP TABLE rates;
DROP TABLE subscribers;

CREATE TABLE rates (
	currid SERIAL PRIMARY KEY,
	currcode VARCHAR(10) NOT NULL,
	currlabel VARCHAR(50) NOT NULL,
	rate NUMERIC NOT NULL,
	last_update TIMESTAMP NOT NULL);

CREATE TABLE subscribers (
	subscriberid SERIAL PRIMARY KEY,
	username VARCHAR(120) NOT NULL,
	pwdhash VARCHAR(120) NOT NULL);