from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint
import requests
import json


def getDevopsClient(personal_access_token,organization_url):
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    core_client = connection.clients.get_core_client()
    return core_client

def getAllProjects(core_client):
    all_projects=[]
    get_projects_response = core_client.get_projects()
    index = 0
    while get_projects_response is not None:
        for project in get_projects_response.value:
            all_projects.append({"id":project.id,"name":project.name,"url":project.url})
            index += 1
            #print(dict(project))
        if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
            # Get the next page of projects
            get_projects_response = core_client.get_projects(continuation_token=get_projects_response.continuation_token)
        else:
            # All projects have been retrieved
            get_projects_response = None
    #print(core_client.get_project(1))

    return all_projects

def getProject(core_client,project_id):
    return core_client.get_project(project_id)

def getWorkItemJsonData(workitem_id,cookie):
    response = requests.get("https://office.visualstudio.com/DefaultCollection/Outlook%20Mobile/_apis/wit/workitems?ids="+str(workitem_id)+"&api-version=5.1", cookies=cookie)
    if(response.status_code==200):
        return json.loads(response.text)
    else:
        print(response.status_code,response.reason)








