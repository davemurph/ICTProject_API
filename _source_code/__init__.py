from flask import Flask

app = Flask(__name__)

# config
app.secret_key = 'development key'

import exchange_api