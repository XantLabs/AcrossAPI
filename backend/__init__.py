"""Main init file. File does not need to be edited except for server edits."""

from url import URLS
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
urlify(app, URLS)
# Just for debug:
# import views
# app.add_url_rule('/test', view_func=views.test, methods=["GET"])

# Set config vars.
UPLOAD_FOLDER = 'media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = secure.DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
db = SQLAlchemy(app)

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
