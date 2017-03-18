"""Libs for uploading to the server."""
import hashlib
from datetime import datetime

FILEHASH = hashlib.sha256()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def hashFile(filename):
    """Hash a filename depending on filename and datetime."""
    utcTime = str(datetime.utcnow())
    inputStr = filename.split('.')[0] + utcTime
    FILEHASH.update(inputStr.encode())

    return FILEHASH.hexdigest()[:16] + '.' + filename.split('.')[1]


def allowed_file(filename):
    """Return whether a file is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
