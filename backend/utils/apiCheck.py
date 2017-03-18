def checkApiKey(apikey):
    open(APIKEY_FILE, 'a').close()
    with open(APIKEY_FILE, 'r') as f:
        for j in [str(i.rstrip()) for i in f.readlines()]:
            if j == apikey.rstrip():
                return True
        return False
