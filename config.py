import json
with open('config.json', 'r') as f:
    data = json.load(f)

def getMyToken():
	return data["token"]

def getMyCookie():
	return data["cookie"]