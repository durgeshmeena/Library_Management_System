import logging
from flask import Flask
from flask_mongoengine import MongoEngine

# from library_management.config import DEBUG

# Logging configuration----------------
# logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
# logging.getLogger().setLevel(logging.DEBUG)
#------------------------------------

app = Flask(__name__, static_url_path='',static_folder='static', )
app.config.from_object('config')
app.config['SECRET_KEY']  = 'hgfds$#2nBGY*^&*isdft549uht4345umnbgfc?65v'
# db = MongoEngine(app)

from app import views
