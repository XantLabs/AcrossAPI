"""Provide views bound to urls. Does not include error handlers."""

import os

from flask import request, send_from_directory, url_for

from utils.upload import *


def upload():
    """Upload a file to the host. Return an error if it fails."""
    # Check if the post request has the file part.
    if 'file' not in request.files:
        return "Forbidden: file part must be included in HTTP POST " + \
            "request.", 403

    file = request.files['file']

    # Filename must be nonempty to be valid.
    if file.filename == '':
        return "Forbidden: cannot upload file with no filename.", 403

    # If the file is allowed, continue. If not, return 403.
    if file and allowed_file(file.filename) and
    checkApiKey(str(request.form['apikey']).rstrip()):
        filename = hashFile(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Upload renamed file to database.

        return url_for('uploaded_file', filename=filename)

    return "Forbidden: ensure the file extension is allowed and API key " +\
        "is correct.", 403


def uploadedFile(filename):
    """Show an uploaded file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
