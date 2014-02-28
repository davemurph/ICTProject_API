# class definition for thread object, used by
# exchange_api.py to get live currency rates
# from Google feed periodically
# (return period = param in time.sleep(), measured in seconds)

from flask import json
from threading import Thread
import requests, time


class RatesThread (Thread):
	def __init__(self):
		'''Constructor'''
		Thread.__init__(self)
		self.exchange_rates = {'EUR': 1.0}
		
	def run(self):
		while True:
			json_live_rates = requests.get('http://spreadsheets.google.com/feeds/list/0Av2v4lMxiJ1AdE9laEZJdzhmMzdmcW90VWNfUTYtM2c/3/public/basic?alt=json')
			live_rates = json_live_rates.json()
			self.exchange_rate_last_update = time.ctime()

			number_of_currencies_in_feed = len(live_rates['feed']['entry'])			
	
			for currency_entry in range(number_of_currencies_in_feed):
				currency = live_rates['feed']['entry'][currency_entry]['title']['$t']
				rate_as_string = live_rates['feed']['entry'][currency_entry]['content']['$t']
				rate = float(rate_as_string[8:])
				
				self.exchange_rates[currency] = rate				
		
			time.sleep(300)