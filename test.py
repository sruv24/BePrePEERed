import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+"/DevOps")
from config import *
from devopsApi import *
import requests

personal_access_token = getMyToken()
my_cookie=getMyCookie()
url_first_part="https://office.visualstudio.com/DefaultCollection/Outlook%20Mobile/"


getAllWorkItems(url_first_part,my_cookie)
#getPrsForWorkItems(url_first_part,my_cookie)
# repo_id="28406b7c-4cef-44f1-bb35-15e73d905ffb"
# pr_id=341909
# url=url_first_part+"_apis/git/repositories/28406b7c-4cef-44f1-bb35-15e73d905ffb/pullRequests/341909?api-version=5.1"
# data=makeGETRequest(url,my_cookie)
# workitem_id=3759461
# workitem=getWorkItemJsonData(url_first_part,workitem_id,my_cookie)
# print(workitem)

# pr_id=workitem["PR_id"]
# print(getPRJsonData(url_first_part,pr_id,my_cookie))
