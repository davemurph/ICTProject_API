from flask.ext.testing import TestCase
import unittest
from _source_code import app
from _source_code.exchange_api import validate_amount


# limited testing using Flask-Testing to demonstrate
# use of testing in Flask

# testing of exposed services completed using cURL

class TestCases(TestCase):

	def create_app(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False		
		return app

	def setUp(self):
		pass


	def tearDown(self):
		pass


	def test_get_currencies_unauthorised_subscriber(self):
		response = self.client.get('testapi/getcurrencies')
		self.assertEquals(response.json, dict(error = 'Unauthorised access'))

	def test_get_currencies_unauthorised_subscriber_status_code_403(self):
		response = self.client.get('testapi/getcurrencies')
		self.assert403(response)

	def test_validate_amount_numerical_value(self):
		valid_output = validate_amount(123.45)
		self.assertTrue(valid_output)

	def test_validate_amount_nonnumeric_valus(self):
		invalid_output = validate_amount('xyz')
		self.assertFalse(invalid_output)
