"""Provide views bound to urls. Does not include error handlers."""

import os

from flask import request, send_from_directory, url_for

UPLOAD_FOLDER = 'media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def upload():
    """Upload a file to the host. Return an error if it fails."""
    # Check if the post request has the file part.
    if 'file' not in request.files:
        flash('No file part')
        abort(403)

    file = request.files['file']

    # Filename must be nonempty to be valid.
    if file.filename == '':
        flash('No selected file')
        abort(403)

    # If the file is allowed, continue. If not, return 403.
    if file and allowed_file(file.filename):
        filename = hashFile(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return url_for('uploaded_file', filename=filename)

    abort(403)


def uploadedFile(filename):
    """Show an uploaded file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
