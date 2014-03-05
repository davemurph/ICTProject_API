# RESTful api (Flask/Python)

# currency conversion
# all data in HTTP methods is JSON format

# getSpecificRate() and exchange() return floats
# getRate() returns a float

# get_active_currency_list() returns currency
# dictionary (JSON format)

# exchange rates are relative to 1.0 * Euro

# code structure adapted from tutorial at 
# http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# by Miguel Grinberg

from _source_code import app
from flask import Flask, jsonify, abort, request, make_response, json
from flask.ext.httpauth import HTTPBasicAuth
import requests
from rates_thread import RatesThread
from decimal import Decimal


auth = HTTPBasicAuth()


live_rates = RatesThread()
live_rates.daemon = True
live_rates.start()

RATE_INDEX = 0
LABEL_INDEX = 1


@auth.get_password
def get_password(username):
	if username == 'daithi':
		return 'pass1234'
	return None


@auth.error_handler
def unauthorized():
	return make_response(jsonify( { 'error': 'Unauthorised access' } ), 403)
	

@app.route('/testapi/convert/<string:currency>', methods = ['GET'])
@auth.login_required
def get_rate(currency):
	if currency in live_rates.exchange_rates:
		return jsonify ( { 'rate': live_rates.exchange_rates[currency] } )
	else:
		abort(404)
		
			
@app.route('/testapi/convert', methods = ['POST'])
@auth.login_required
def convert_amount():
	if not request.json:
		abort(400)

	if not 'from_currency' in request.json:
		abort(400)

	if not 'to_currency' in request.json:
		abort(400)

	if not 'amount' in request.json:
		abort(400)
		
	if not validate_amount(request.json['amount']):
		abort(400)
		
	if request.json['from_currency'] not in live_rates.exchange_rates:
		abort(404)

	if request.json['to_currency'] not in live_rates.exchange_rates:
		abort(404)

	
	converted_amount = exchange(request.json['from_currency'], 
								request.json['to_currency'], 
								request.json['amount'])

	unit_rate = get_unit_rate(request.json['from_currency'],
							  request.json['to_currency'])

	return jsonify( { 'converted_amount': converted_amount, 
					  'unit_rate': unit_rate, 
					  'last_update': live_rates.exchange_rate_last_update } )


@app.route('/testapi/getcurrencies', methods = ['GET'])
@auth.login_required
def get_active_currency_list():
	currency_list = {}
	for currency_code in live_rates.exchange_rates:
		currency_list[currency_code] = live_rates.exchange_rates[currency_code][LABEL_INDEX]
		
	return jsonify ( { 'currency_list': currency_list } )


@app.errorhandler(404)
def not_found(error):
		return make_response(jsonify( { 'error': 'Resource not found' } ), 404)
		
		
@app.errorhandler(400)
def bad_request(error):
		return make_response(jsonify( { 'error': 'Bad request' } ), 400)
		

def get_unit_rate(from_currency, to_currency):
	from_rate = live_rates.exchange_rates[from_currency][RATE_INDEX]		
	to_rate = live_rates.exchange_rates[to_currency][RATE_INDEX]

	decimal_from_rate = Decimal(from_rate)
	decimal_to_rate = 	Decimal(to_rate)

	decimal_unit_rate = decimal_to_rate / decimal_from_rate
		
	# return a string for JSON string
	return str(decimal_unit_rate)
	
			
def exchange(from_currency, to_currency, amount):
	from_rate = live_rates.exchange_rates[from_currency][RATE_INDEX]		
	to_rate = live_rates.exchange_rates[to_currency][RATE_INDEX]

	decimal_from_rate = Decimal(from_rate)
	decimal_to_rate = 	Decimal(to_rate)
	decimal_amount = 	Decimal(amount)

	decimal_converted_amount = decimal_amount * decimal_to_rate / decimal_from_rate

	# return a string for JSON string		
	return str(decimal_converted_amount)
	

# validate value of key 'amount' as numerical string	
def validate_amount(amount):
	try:
		float(amount)
		return True
	except ValueError:
		return False
