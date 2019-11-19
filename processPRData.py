import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+"/DevOps")
from config import *
from devopsApi import *
import requests

OMworkItemsDataFile="data/OMworkitemsdata.json"
workItemsData=fetchStoredData(workItemsDataFile)

OMprDataFile="data/OMprdata.json"
prData=fetchStoredData(OMprDataFile)

devDataFile="data/devdataOverall.json"
devData=fetchStoredData(devDataFile)

def getWorkItemForPR(pr_id):
	for w in workItemsData:
		if "PR_id" in w and w["PR_id"]==pr_id:
			return w

def getAllDevelopers():
	return list(devData.keys())

def addScoreDeveloper(devName,score):
	print("\t",devName,score)
	if devName in devData:
		devData[devName]+=score
	else:
		devData[devName]=score

def scoreDevForPr(prItem):
	workItem=getWorkItemForPR(prItem["Id"])
	prio=3
	if "Priority" in workItem:
		prio=workItem["Priority"]
	print("PR ",prItem["Id"]," WI ",workItem["Id"]," prio ",prio)
	addScoreDeveloper(prItem["createdBy"],(1/prio)*10)
	if "reviewers" in prItem:
		for rev in prItem["reviewers"]:
			addScoreDeveloper(rev,(1/prio)*20)


def scoreAllPrs():
	for i,prItem in enumerate(prData):
		scoreDevForPr(prItem)
		if(i%10==0):
			print("dumping..")
			dumpJsonData(devData,devDataFile)
	dumpJsonData(devData,devDataFile)

#scoreAllPrs()
devs=sorted(devData,reverse=True)
for d in devs:
	print(d,devData[d])
#scoreAllPrs()


