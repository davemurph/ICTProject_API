from flask.ext.testing import TestCase
import unittest
from _source_code import app

class SimpleApiTest(TestCase):

	SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:david1979@localhost/exch_rates_db"
	TESTING = True

	def create_app(self):		
		app.config['TESTING'] = True
		return app

	def test_get_currencies(self):
		response = self.client.get('/testapi/getcurrencies')
		print response.json

if __name__ == '__main__':
	unittest.main()