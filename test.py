import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+"/DevOps")
from config import *
from devopsApi import *

personal_access_token = getMyToken()
organization_url = 'https://dev.azure.com/office'

devopsClient = initialiseDevops(personal_access_token,organization_url)
allProjects=getAllProjects(devopsClient)
print(allProjects)