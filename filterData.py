import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+"/DevOps")
from config import *
from devopsApi import *
import requests


# workItemsDataFile="data/workitemsdata.json"
# prDataFile="data/prdata.json"

# workItemsData=fetchStoredData(workItemsDataFile)
# prData=fetchStoredData(prDataFile)

teamProjectsDict={}
for w in workItemsData:
	tp=w["TeamProject"]
	if tp not in teamProjectsDict:
		teamProjectsDict[tp]=1
	else:
		teamProjectsDict[tp]+=1

#{'OC': 147, 'OneNote': 10, 'GSX': 9, 'Outlook Mobile': 8761, 'OE': 16, 'APEX': 16, 'MAX': 9, 'Project': 6, 'Universal Outlook': 5, 'CLE': 5}		

omData=[w for w in workItemsData if w["TeamProject"]=="Outlook Mobile"]
prIds=[w["PR_id"] for w in omData if "PR_id" in w] 
omPrData=[p for p in prData if p["Id"] in prIds]

print(len(omData),len(omPrData))


OMworkItemsDataFile="data/OMworkitemsdata.json"
OMprDataFile="data/OMprdata.json"

dumpJsonData(omData,OMworkItemsDataFile)
dumpJsonData(omPrData,OMprDataFile)