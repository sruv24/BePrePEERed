import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+"/DevOps")
from config import *
from devopsApi import *
import requests

personal_access_token = getMyToken()
my_cookie=getMyCookie()

workitem_id=3678529
url_first_part="https://office.visualstudio.com/DefaultCollection/Outlook%20Mobile/"
workitem=getWorkItemJsonData(url_first_part,workitem_id,my_cookie)
print(workitem)
