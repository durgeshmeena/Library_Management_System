import os
from os import environ
from dotenv import load_dotenv, find_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
import certifi
#---------------------------------
# Default Config
#---------------------------------

DEBUG = False


# Loading secretes from .env file
load_dotenv(find_dotenv())

# APP_SECRETE
SECRETE_KEY = environ.get('SECRETE_KEY')

# MongoDB setting
MONGODB_SETTINGS = {'DB':'LibM', 'host':environ.get('MONGO_URI'),'tlsCAFile':certifi.where()}

# Flask-WTF flag for CSRF
CSRF_ENABLED = True

#-----------------------------
