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
from flask import Flask, jsonify, abort, request, make_response, json, flash, render_template
from flask.ext.httpauth import HTTPBasicAuth
import requests
from rates_thread import RatesThread
from decimal import Decimal
from models import Subscriber, StoredRate
from database import db_session
from forms import AddSubscriber


auth = HTTPBasicAuth()


live_rates = RatesThread()
live_rates.daemon = True
live_rates.start()


@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()


@auth.verify_password
def verify_password(username, password):
	subscriber = Subscriber.query.filter_by(username = username).first()
	if subscriber is None:
		return False
	return subscriber.check_password(password)


@auth.error_handler
def unauthorized():
	return make_response(jsonify( { 'error': 'Unauthorised access' } ), 403)
	

@app.route('/currencyapi/addsubscriber', methods = ['GET', 'POST'])
def add_subscriber():
	form = AddSubscriber()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('apiadmin.html', form = form)

		else:
			new_subscriber = Subscriber(form.username.data, form.password.data)
			db_session.add(new_subscriber)
			db_session.commit()
			flash('New subscriber added')

			return render_template('apiadmin.html', form = form)

	elif request.method == 'GET':
		return render_template('apiadmin.html', form = form)


@app.route('/currencyapi/convert', methods = ['POST'])
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
		
	converted_amount = exchange(request.json['from_currency'], 
								request.json['to_currency'], 
								request.json['amount'])

	unit_rate = get_unit_rate(request.json['from_currency'],
							  request.json['to_currency'])

	exchange_rate_last_update = StoredRate.query.order_by(StoredRate.last_update.desc()).first().last_update

	return jsonify( { 'converted_amount': converted_amount, 
					  'unit_rate': unit_rate, 
					  'last_update': exchange_rate_last_update } )


@app.route('/currencyapi/getcurrencies', methods = ['GET'])
@auth.login_required
def get_active_currency_list():
	currency_list = {}

	min_currency_id = StoredRate.query.order_by(StoredRate.currid).first().currid	
	number_of_available_currencies = StoredRate.query.count()	
	
	for currency_record in range(min_currency_id, min_currency_id + number_of_available_currencies):
		currency = StoredRate.query.filter_by(currid = currency_record).first()

		currency_list[currency.currcode] = currency.currlabel

	return jsonify ( { 'currency_list': currency_list } )


@app.errorhandler(404)
def not_found(error):
		return make_response(jsonify( { 'error': 'Resource not found' } ), 404)
		
		
@app.errorhandler(400)
def bad_request(error):
		return make_response(jsonify( { 'error': 'Bad request' } ), 400)
		

def get_unit_rate(from_currency, to_currency):
	from_currency_listing = StoredRate.query.filter_by(currcode = from_currency).first()
	to_currency_listing = StoredRate.query.filter_by(currcode = to_currency).first()

	from_rate = from_currency_listing.rate
	to_rate = to_currency_listing.rate

	decimal_from_rate = Decimal(from_rate)
	decimal_to_rate = 	Decimal(to_rate)

	decimal_unit_rate = decimal_to_rate / decimal_from_rate
		
	# return a string for JSON string
	return str(decimal_unit_rate)
	
			
def exchange(from_currency, to_currency, amount):
	from_currency_listing = StoredRate.query.filter_by(currcode = from_currency).first()
	to_currency_listing = StoredRate.query.filter_by(currcode = to_currency).first()

	from_rate = from_currency_listing.rate
	to_rate = to_currency_listing.rate

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