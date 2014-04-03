-- create users psql database for Currency Converter Client
-- user already exists
-- must login to psql as follows: >psql -d template1 -U postgres

DROP DATABASE exch_rates_db;

CREATE DATABASE exch_rates_db;
GRANT ALL PRIVILEGES ON DATABASE exch_rates_db TO daithi;