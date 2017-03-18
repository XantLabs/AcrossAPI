"""Main init file."""

import views

from flask import Flask
from utils.generalutils import urlify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
DEBUG = True
limiter = Limiter(
    app,
    key_func=get_remote_address,
    global_limits=["10000 per hour"]
)

# Map URLs to view functions. Allows more modular code.
URLS = [
    ('/', views.index),
]

urlify(app, URLS)

# Custom error handlers.


@app.errorhandler(403)
def fourOhThree(e):
    """Provide standardised string error message as response."""
    return "Access denied. Insufficient permissions.", 403


@app.errorhandler(404)
def fourOhFour(e):
    """Provide standardised string error message as response."""
    return "Not found. What you are looking for doesn't exist.", 404


@app.errorhandler(410)
def fourTen(e):
    """Provide standardised string error message as response."""
    return "The file was here before, but now it's gone.", 410


@app.errorhandler(500)
def fiveHundred(e):
    """Provide standardised string error message as response."""
    return "Internal server error. Some dev messed up.", 500
