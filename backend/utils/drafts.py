#testing random bits of code
from datetime import datetime
import hashlib

FILEHASH = hashlib.sha256()

def hash(filename):

    utcTime = str(datetime.utcnow())
    print(filename)
    print(filename.split('.')[0])
    inputStr = filename.split('.')[0] + utcTime
    FILEHASH.update(inputStr.encode())
    return FILEHASH.hexdigest() +'.'+filename.split('.')[1]

print (hash("test.jpeg"))
