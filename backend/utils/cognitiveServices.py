"""Microsoft Azure libraries."""

import base64
import datetime
import json
import time
import urllib.error
import urllib.parse
import urllib.request

import http.client

last_authTime = None
auth = None

# returns True if 'adult content' otherwise False.


def isModerate(imageurl):
    """Find if an image is moderated."""
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'fcf357ac9e914add9d43c53cb8b57f38',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'CacheImage': 'False',
    })

    try:
        endpoint = 'westus.api.cognitive.microsoft.com'
        conn = http.client.HTTPSConnection(endpoint)
        body = json.dumps({"DataRepresentation": "URL", "Value": imageurl})
        conn.request("POST",
                     "/contentmoderator/moderate/v1.0/ProcessImage/Evaluate?%s"
                     % params, body, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        return data["IsImageAdultClassified"]
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def getAuth():
    """Get auth."""
    global auth
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'ffe39cd4f6004341b4d1271a085abe99',
    }
    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("POST", "/sts/v1.0/issueToken", '{body}', headers)
        response = conn.getresponse()
        auth = str(response.read(), 'utf-8')
        # auth = base64.b64encode(response.read())
        return auth

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

# returns string of translated caption


def translate(caption, translateFrom, translateTo):
    """Translate a string from a given language to another given language."""
    global last_authTime
    global auth
    if (last_authTime is None):
        last_authTime = datetime.datetime.now()
        auth = getAuth()
    elif (datetime.datetime.now() - last_authTime).seconds > 550:
        last_authTime = datetime.datetime.now()
        auth = getAuth()

    translate_packet = {
        'text': caption,
        'to': translateTo,
        'from': translateFrom
    }

    headers = {
        # Request headers
        'Authorization': 'Bearer ' + auth,
    }

    try:
        url = "/v2/http.svc/Translate?%s"
        conn = http.client.HTTPSConnection('api.microsofttranslator.com')
        conn.request("GET", url % urllib.parse.urlencode(
            translate_packet), '{body}', headers)
        response = conn.getresponse()
        data = str(response.read(), 'utf-8')
        data = data.partition('>')[-1].rpartition('<')[0]

        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
