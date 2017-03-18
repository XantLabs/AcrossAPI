"""Main init file. File does not need to be edited except for server edits."""

import url
import secure
import models

from flask import Flask
from utils.generalutils import urlify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Run server and rate limit.
app = Flask(__name__)
DEBUG = True
limiter = Limiter(
    app,
    key_func=get_remote_address,
    global_limits=["10000 per hour"]
)

# Set URLs to views
urlify(app, url.URLS)

# Set config vars.
UPLOAD_FOLDER = 'media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + \
    'root@localhost/swagswag'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
db = SQLAlchemy(app)

# Social authentication information
app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': secure.APP_ID,
    'consumer_secret': secure.APP_SECRET
}

# Custom error handlers


@app.errorhandler(403)
def fourOhThree(e):
    """Provide standardised string error message as response."""
    return "Access denied. Insufficient permissions for request.", 403


@app.errorhandler(404)
def fourOhFour(e):
    """Provide standardised string error message as response."""
    return "Not found. What you are looking for doesn't exist.", 404


@app.errorhandler(410)
def fourTen(e):
    """Provide standardised string error message as response."""
    return "Not found. The file was here before, but now it's gone.", 410


@app.errorhandler(500)
def fiveHundred(e):
    """Provide standardised string error message as response."""
    return "Internal server error. One of our devs messed up.", 500

# Other views are located in views.py.
