import json
import os
with open('config.json', 'r') as f:
    data = json.load(f)

def getMyToken():
	return data["token"]

def getMyCookie():
	return data["cookie"]

if os.path.exists("data/workitemsdata.json")==False:
	with open("data/workitemsdata.json", 'w') as f:
		json.dump([],f)

if os.path.exists("data/prdata.json")==False:
	with open("data/prdata.json", 'w') as f:
		json.dump([],f)