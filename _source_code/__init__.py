from flask import Flask

# config
app = Flask(__name__)
app.secret_key = 'development key'

# import routes
import exchange_api