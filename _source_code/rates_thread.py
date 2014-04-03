# class definition for thread object, used by
# exchange_api.py to get live currency rates
# from Google feed periodically
# (return period = parameter in time.sleep(), measured in seconds)

from flask import json
from threading import Thread
import requests, time
from models import StoredRate
from database import db_session
from configobj import ConfigObj


# config data
config = ConfigObj('config_settings.ini')
thread_sleep_time = int(config['live_currency_feed']['thread_sleep_time'])


class RatesThread (Thread):
	# labels for Top 10 currency codes provided by free live feed service
	currency_codes = {	'EUR': 'Euro', 
						'USD': 'US Dollar',
						'JPY': 'Japanese Yen', 
						'GBP': 'British Pound',
						'CHF': 'Swiss Franc', 
						'AUD': 'Australian Dollar',
						'CAD': 'Canadian Dollar',
						'SEK': 'Swedish Krona',
						'HKD': 'Hong Kong Dollar',
						'NOK': 'Norwegian Krone'}

	def __init__(self):
		'''Constructor'''
		Thread.__init__(self)

		
	def run(self):
		while True:
			try:

				json_live_rates = requests.get('http://spreadsheets.google.com/feeds/list/0Av2v4lMxiJ1AdE9laEZJdzhmMzdmcW90VWNfUTYtM2c/3/public/basic?alt=json')
				live_rates = json_live_rates.json()
				exchange_rate_last_update = time.ctime()

				euro_listing = StoredRate('EUR', 'Euro', 1.000, exchange_rate_last_update)
				euro_in_store = StoredRate.query.filter_by(currcode = 'EUR').first()

				if euro_in_store is None:
					db_session.add(euro_listing)
				else:
					euro_in_store.last_update = exchange_rate_last_update

				number_of_currencies_in_feed = len(live_rates['feed']['entry'])			
	
				for currency_entry in range(number_of_currencies_in_feed):
					currency_code = live_rates['feed']['entry'][currency_entry]['title']['$t']
				
					if currency_code in self.currency_codes:
						currency_label = self.currency_codes[currency_code]

					rate = live_rates['feed']['entry'][currency_entry]['content']['$t'][8:]

					currency_in_store = StoredRate.query.filter_by(currcode = currency_code).first()
					if currency_in_store is None:
						new_currency = StoredRate(currency_code, currency_label, rate, exchange_rate_last_update)
						db_session.add(new_currency)
					else:
						currency_in_store.rate = rate
						currency_in_store.last_update = exchange_rate_last_update
				
				db_session.commit()

				time.sleep(thread_sleep_time)

			except:
				print 'Currency feed connection error. Retry in ' + str((int(thread_sleep_time) / 60.0)) + ' minutes.'
				time.sleep(thread_sleep_time)