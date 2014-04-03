# code taken from SQLAlchemy documentation
# http://flask.pocoo.org/docs/patterns/sqlalchemy/#declarative

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_uri = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres:pass1234@localhost/exch_rates_db') 
engine = create_engine(database_uri, convert_unicode = True)
db_session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


'''
db_session.connection().connection.set_isolation_level(0)
db_session.execute('CREATE DATABASE exch_rates_db')
db_session.connection().connection.set_isolation_level(1)'''


def init_db():
	import models
	Base.metadata.create_all(bind=engine)