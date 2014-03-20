from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	userid = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), unique = True)
	pwdhash = db.Column(db.String(120))

	def __init__(self, email, password):
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)