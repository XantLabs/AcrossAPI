"""Provide views bound to urls. Does not include error handlers."""

import datetime
import os

from flask import request, send_from_directory, url_for

from models import Photo, db
from utils import pipeline
from utils.upload import *


def upload():
    """Upload a file to the host. Return an error if it fails."""
    # Check if the post request has the file part.
    if 'file' not in request.files:
        return "Forbidden: file part must be included in HTTP POST " + \
            "request.", 403

    file = request.files['file']
    caption = request.form['caption']
    language = request.form['language']
    lat = request.form['lat']
    lon = request.form['lon']

    # Filename must be nonempty to be valid.
    if file.filename == '':
        return "Forbidden: cannot upload file with no filename.", 403

    # If the file is allowed, continue. If not, return 403.
    if file and allowed_file(file.filename) and checkApiKey(
            str(request.form['apikey']).rstrip()):
        filename = hashFile(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Upload renamed file to database.
        newPhoto = Photo(datetime.datetime.utcnow, caption, language, 0,
                         filename, lat, lon, 0, 0)

        return url_for('uploaded_file', filename=filename)

    return "Forbidden: ensure the file extension is allowed and API key " + \
        "is correct.", 403


def uploadedFile(filename):
    """Show an uploaded file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def sendTopPhotos():
    """From a POST request send n photos in JSON format to the requestee."""
    n = request.form['n']  # number of photos, max.
