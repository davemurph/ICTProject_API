from flask import Flask
from models import db

app = Flask(__name__)

# config
app.secret_key = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://daithi:david1979@localhost/pythondb'

db.init_app(app)


import exchange_api