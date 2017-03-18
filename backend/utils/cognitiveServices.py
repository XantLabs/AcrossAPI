import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

# returns True if 'adult content' otherwise False.
def isModerate(imageurl):

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
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        body = json.dumps({ "DataRepresentation":"URL","Value":imageurl})
        conn.request("POST",
                     "/contentmoderator/moderate/v1.0/ProcessImage/Evaluate?%s"
                     % params, body, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        return data["IsImageAdultClassified"]
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

#not yet implemented
def captionTranslation():
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'ffe39cd4f6004341b4d1271a085abe99',
    }
    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("POST", "/sts/v1.0/issueToken",'{body}' ,headers)
        response = conn.getresponse()
        auth = response.read()
        print (auth)
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

#for debugging
print(isModerate('http://i.imgur.com/qEzKzk9.jpg'))
captionTranslation()
