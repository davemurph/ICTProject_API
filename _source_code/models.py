from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql+psycopg2://daithi:david1979@localhost/exch_rates_db')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Subscriber(Base):
	__tablename__ = 'subscribers'
	subscriberid = Column(Integer, primary_key = True)
	username = Column(String(120), unique = True)
	pwdhash = Column(String(120))

	def __init__(self, username, password):
		self.username = username.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)


class StoredRate(Base):
	__tablename__ = 'rates'
	currid = Column(Integer, primary_key = True)
	currcode = Column(String(10))
	currlabel = Column(String(50))
	rate = Column(Numeric)
	last_update = Column(DateTime)

	def __init__(self, currcode, currlabel, rate, last_update):
		self.currcode = currcode
		self.currlabel = currlabel
		self.rate = rate
		self.last_update = last_update