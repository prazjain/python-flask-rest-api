from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////LOCAL/Data/github/python/python-flask-rest-api/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
