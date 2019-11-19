import pprint
import requests
import json
import random
import pandas as pd

workItemsDataFile="data/workitemsdata.json"
prDataFile="data/prdata.json"
queriedWorkItemsDataFile="data/QueriedWorkItems.csv"


def fetchStoredData(file):
    data=[]
    with open(file) as f:
        data = json.load(f)
    print("Loaded from file : ",file,len(data))
    return data

workItemsData=fetchStoredData(workItemsDataFile)
prData=fetchStoredData(prDataFile)

def dumpJsonData(data,file):
    with open(file,"w") as f:
        json.dump(data, f)

def getAllQueriedWorkIDs():
    df=pd.read_csv(queriedWorkItemsDataFile)
    return df["ID"].tolist()


def makeGETRequest(url,cookie):
    response = requests.get(url, cookies=cookie)
    if(response.status_code==200):
        return json.loads(response.text)
    # else:
    #     print(response.status_code,response.reason)




def getCommentUrl(workitemdata):
    data=workitemdata["value"][0]
    links=data["_links"]
    if("workItemComments") in links:
        comments=links["workItemComments"]["href"]
        return comments

def parseCommentsData(commentJsonData):
    return [c["text"] for c in commentJsonData["comments"]]



def getWorkItemJsonData(url_first_half,workitem_id,cookie):
    url=url_first_half+"_apis/wit/workitems?ids="+str(workitem_id)+"&$expand=all&api-version=5.1"
    #print(url)
    data=makeGETRequest(url,cookie)
    if(data):
        return parseWorkItemData(url_first_half,data,cookie)

def parseWorkItemData(url_first_half,workitemdata,cookie):
    data=workitemdata["value"][0]
    new_data={}
    fields=data["fields"]
    fields_keys=["System.Id",'System.TeamProject',"System.WorkItemType","System.Title","System.Description","Microsoft.VSTS.TCM.ReproSteps","Office.Common.ExpectedOutcome","Office.Common.ActualOutcome","System.Tags",'System.WorkItemType','Microsoft.VSTS.Common.Priority']
    #print(fields.keys())
    for k in fields_keys:
        if k in fields:
            new_k=k.replace("System.","").replace("Microsoft.VSTS.TCM.","").replace("Office.Common.","").replace("Microsoft.VSTS.Common.","")
            new_data[new_k]=fields[k]
    comment_url=getCommentUrl(workitemdata)
    if(comment_url):
        commentJsonData=makeGETRequest(comment_url,cookie)
        comments={"Comments":parseCommentsData(commentJsonData)}
        new_data.update(comments)
    pr_id=getPullRequestID(workitemdata)
    if(pr_id):
        new_data.update({"PR_id":pr_id})
    return new_data

def getPullRequestID(workitemdata):
    data=workitemdata["value"][0]
    relations=data["relations"]
    for r in relations:
        if r["rel"]=="ArtifactLink" and r["attributes"]["name"]=='Pull Request':
            pr_url=r["url"]
            #print(r)
            return pr_url[-6:]

def getPRJsonData(url_first_half,pr_id,cookie,repoData):
    for r in repoData:
        repo_id=r["Id"]
        url=url_first_half+"_apis/git/repositories/"+repo_id+"/pullRequests/"+pr_id+"?api-version=5.1"
        #print(url)
        data=makeGETRequest(url,cookie)
        if(data):
            return parsePRData(data,pr_id)

def parsePRData(prData,pr_id):
    new_data={}
    new_data["Id"]=pr_id
    new_data["createdBy"]=prData["createdBy"]["uniqueName"]
    new_data["title"]=prData["title"]
    if "description" in prData:
        new_data["description"]=prData["description"]
    new_data["reviewers"]=[r["uniqueName"] for r in prData["reviewers"]]
    return new_data

def getAllWorkItems(url_first_half,cookie,repoData):
    existing_workitem_ids=[s["Id"] for s in workItemsData]
    all_workitem_ids=getAllQueriedWorkIDs()
    count=0
    #while count < 200:
    for work_item_id in all_workitem_ids:
        #work_item_id=random.randint(3000000, 5000000) 
        if work_item_id not in existing_workitem_ids:
            try:
                workitemdata=getWorkItemJsonData(url_first_half,work_item_id,cookie)
                if(workitemdata):
                    print(count,":",work_item_id ," SUCCESS")
                    workItemsData.append(workitemdata)
                    if "PR_id" in workitemdata:
                        pr_data = getPRJsonData(url_first_half,workitemdata["PR_id"],cookie,repoData)
                        if(pr_data):
                            print("\t PR SUCCESS")
                            prData.append(pr_data)
                else:
                    print(count,":",work_item_id ," FAILED")

            except Exception as e:
                print(count,":",work_item_id ," FAILED ")
        #work_item_id+=1
        count+=1
        if count%200==0:
            dumpJsonData(workItemsData,workItemsDataFile)
            dumpJsonData(prData,prDataFile)
    dumpJsonData(workItemsData,workItemsDataFile)
    dumpJsonData(prDataFile,prData)


def getPrsForWorkItems(url_first_half,cookie,repoData):
    existing_pr_ids=[s["Id"] for s in prData]
    for i,workitem in enumerate(workItemsData):
        #print(workitem)
        if("PR_id" in workitem):
            pr_id=workitem["PR_id"]
            print(pr_id)
            if pr_id not in existing_pr_ids:
                pr_data = getPRJsonData(url_first_half,pr_id,cookie,repoData)
                if(pr_data):
                    print(" SUCCESS")
                    prData.append(pr_data)
        if i%10==0:
            print("dumpimg...")
            dumpJsonData(prData,prDataFile)
    dumpJsonData(prData,prDataFile)

def redoWorkItems(url_first_half,cookie):
    oldworkItemsData=fetchStoredData("data/workitemsdataOLD.json")
    existing_workitem_ids=[s["Id"] for s in oldworkItemsData]
    count=0
    for work_item_id in existing_workitem_ids:
        try:
            workitemdata=getWorkItemJsonData(url_first_half,work_item_id,cookie)
            if(workitemdata):
                print(count,":",work_item_id ," SUCCESS")
                workItemsData.append(workitemdata)
                if "PR_id" in workitemdata:
                    pr_data = getPRJsonData(url_first_half,workitemdata["PR_id"],cookie)
                    if(pr_data):
                        print("\t PR SUCCESS")
                        prData.append(pr_data)
            else:
                print(count,":",work_item_id ," FAILED")

        except Exception as e:
            print(count,":",work_item_id ," FAILED ")
        count+=1
    dumpJsonData(workItemsData,workItemsDataFile)
    dumpJsonData(prDataFile,prData)

def keepUniqueData():
    newWorkItemsData=[]
    newIds=[]
    for w in workItemsData:
        if w["Id"] not in newIds:
            newWorkItemsData.append(w)
            newIds.append(w["Id"])
    newprData=[]
    newIds=[]
    for w in prData:
        if w["Id"] not in newIds:
            prData.append(w)
            newIds.append(w["Id"])
    dumpJsonData(workItemsData,workItemsDataFile)
    dumpJsonData(prDataFile,prData)

def parseRepoData(data):
    data=data["value"]
    repoData=[]
    for d in data:
        repoData.append({
            "Id":d["id"],"repoName":d["name"]
            })
    return repoData

def getRepoData(cookie):
    url="https://dev.azure.com/office/Outlook%20Mobile/_apis/git/repositories?api-version=5.1"
    data=makeGETRequest(url,cookie)
    if(data):
        return parseRepoData(data)

