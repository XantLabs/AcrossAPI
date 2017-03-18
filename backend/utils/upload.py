"""Libs for uploading to the server."""
import hashlib
import os
import random
import string
from datetime import datetime

FILEHASH = hashlib.sha256()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
APIKEY_FILE = "api.keys"


def genRandomString():
    """Generates a random string."""
    return ''.join(random.choice(string.lowercase) for i in range(10))


def hashFile(filename):
    """Hash a filename depending on filename and datetime."""
    utcTime = str(datetime.utcnow()) + genRandomString()
    inputStr = filename.split('.')[0] + utcTime
    FILEHASH.update(inputStr.encode())

    return FILEHASH.hexdigest()[:16] + '.' + filename.split('.')[1]


def allowed_file(filename):
    """Return whether a file is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def checkApiKey(apikey):
    """Check if an api key provided is good."""
    with open(APIKEY_FILE, 'r') as f:
        for j in [str(i.rstrip()) for i in f.readlines()]:
            if j == apikey.rstrip():
                return True
        return False
