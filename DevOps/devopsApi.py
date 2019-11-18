import pprint
import requests
import json

workItemsDataFile="data/workitemsdata.json"
workItemsData=[]
with open(workItemsDataFile) as f:
    workItemsData = json.load(f)

print("Loaded workItemsData : ",len(workItemsData) )

def makeGETRequest(url,cookie):
    response = requests.get(url, cookies=cookie)
    if(response.status_code==200):
        return json.loads(response.text)
    else:
        print(response.status_code,response.reason)




def getCommentUrl(workitemdata):
    data=workitemdata["value"][0]
    links=data["_links"]
    if("workItemComments") in links:
        comments=links["workItemComments"]["href"]
        return comments

def parseCommentsData(commentJsonData):
    return [c["text"] for c in commentJsonData["comments"]]

def getPullRequestID(workitemdata):
    data=workitemdata["value"][0]
    relations=data["relations"]
    for r in relations:
        if r["rel"]=="ArtifactLink" and r["attributes"]["name"]=='Pull Request':
            pr_url=r["url"]
            #print(r)
            return pr_url[-6:]

# def getPullRequestJsonData(url_first_half,pr_id):
#     url=url_first_half+"_apis/wit/workitems?ids="+str(workitem_id)+"&$expand=all&api-version=5.1"
#     data=makeGETRequest(url,cookie)
#     if(data):
#         return parseWorkItemData(data,cookie)

def getWorkItemJsonData(url_first_half,workitem_id,cookie):
    url=url_first_half+"_apis/wit/workitems?ids="+str(workitem_id)+"&$expand=all&api-version=5.1"
    data=makeGETRequest(url,cookie)
    if(data):
        return parseWorkItemData(url_first_half,data,cookie)

def parseWorkItemData(url_first_half,workitemdata,cookie):
    data=workitemdata["value"][0]
    new_data={}
    fields=data["fields"]
    fields_keys=["System.WorkItemType","System.Title","System.Description","Microsoft.VSTS.TCM.ReproSteps","Office.Common.ExpectedOutcome","Office.Common.ActualOutcome","System.Tags"]
    for k in fields_keys:
        if k in fields:
            new_k=k.replace("System.","").replace("Microsoft.VSTS.TCM.","").replace("Office.Common.","")
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


def getAllWorkItems(url_first_half,cookie):
    work_item_id= 3678529
    count=0
    while work_item_id < 3678531:
        try:
            workitemdata=getWorkItemJsonData(url_first_half,work_item_id,cookie)
            if(workitemdata):
                print(work_item_id ," SUCCESS")
                count+=1
                workItemsData.append(workitemdata)
            else:
                print(work_item_id ," FAILED")

        except Exception as e:
            print(work_item_id ," FAILED ")
        work_item_id+=1
    with open(workItemsDataFile,"w") as f:
        json.dump(workItemsData, f)




