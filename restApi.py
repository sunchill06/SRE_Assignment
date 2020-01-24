#!/bin/python

__author__ = "Sunil Aggarwal"

import requests
import sys
import json
import os
import copy
import argparse
import uuid
import ConfigParser


#Fetch Temporary Access Token for API Client to talk to the Controller. To be Provided by APM Central team.

#TODO : API/Automate the process to aquire Access Token

#AccessToken="eyJraWQiOiI0NTYwODUwZS0zY2U0LTRmYmQtYWJjZS02OWEyYjNlN2IwYjkiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBcHBEeW5hbWljcyIsImF1ZCI6IkFwcERfQVBJcyIsImp0aSI6IjAwTV9DNEt1UnhUY2lPdUZIZFZoMUEiLCJzdWIiOiJyZXN0QVBJQ2xpZW50IiwiaWRUeXBlIjoiQVBJX0NMSUVOVCIsImlkIjoiNDFiMTYxYWUtZjI2OC00Y2IzLWIxZTMtNjFjMmNjMGUwMGE4IiwiYWNjdElkIjoiNDU2MDg1MGUtM2NlNC00ZmJkLWFiY2UtNjlhMmIzZTdiMGI5IiwidG50SWQiOiI0NTYwODUwZS0zY2U0LTRmYmQtYWJjZS02OWEyYjNlN2IwYjkiLCJhY2N0TmFtZSI6Im5hdHdlc3QiLCJ0ZW5hbnROYW1lIjoiIiwiZm1tVG50SWQiOm51bGwsImFjY3RQZXJtIjpbXSwiaWF0IjoxNTc2NDczMDE4LCJuYmYiOjE1NzY0NzI4OTgsImV4cCI6MTYwODAwOTAxOCwidG9rZW5UeXBlIjoiQUNDRVNTIn0.cIPKDYbJ3QzPgiVqSy0dsmwHjhza1KVahaf7R3nRCaI"

########################################################################################
#########     API to fetch Application Details (By CI Number)         ###########
########################################################################################
def getAppNamesByCI(CINumber):
  endpoint="https://natwest.saas.appdynamics.com/controller/rest/applications?output=json"
  headers={'Authorization': 'Bearer {0}'.format(AccessToken)}

  resp=requests.get(endpoint, headers=headers)
  if resp.status_code != 200:
      print("Something went wrong")
      #raise ApiError('GET /controller/rest/applications/<ApplicationName> {}'.format(resp.status_code))

  appDetails={item['name']:item['id'] for item in resp.json() if CINumber in item['name']}

  if appDetails:
    return appDetails
  else:
    print "No Matching Applications found"
    sys.exit()

########################################################################################
#########     API to fetch Application Details (By Application Name)         ###########
########################################################################################

def getAppIdByName():
  endpoint="https://natwest.saas.appdynamics.com/controller/rest/applications/{0}?output=json".format(AppName)
  headers={'Authorization': 'Bearer {0}'.format(AccessToken)}

  resp=requests.get(endpoint, headers=headers)
  #print("Response Code: ",resp.status_code)

  if resp.status_code != 200:
      print("Something went wrong")
      #raise ApiError('GET /controller/rest/applications/<ApplicationName> {}'.format(resp.status_code))

  appData=json.loads(resp.content.decode('utf-8'))
  #print(appData)
  #print("appData ::", appData[0]['id'])

  appId=appData[0]['id']
  return appId


########################################################################################
###############            API to fetch Role (By Role Name)               ##############
########################################################################################

def getRoleInfoByName(TemplateRoleName):
  #TODO: Put a check that this role Exists, Raise an Error if it doesn't

  endpoint="https://natwest.saas.appdynamics.com/controller/api/rbac/v1/roles/name/{0}?include-permissions=true".format(TemplateRoleName)
  headers={'Authorization': 'Bearer {0}'.format(AccessToken)}

  resp=requests.get(endpoint, headers=headers)
  #print("Response Code: ",resp.status_code)

  if resp.status_code != 200:
      print("Something went wrong")
      #raise ApiError('GET /controller/rest/applications/<ApplicationName> {}'.format(resp.status_code))

  #Writing the Role JSON Data to a file
  roleDumpFile=TemplateRoleName+'.txt'
  with open(roleDumpFile, 'w') as outfile:
      json.dump(resp.json(), outfile)

  #print(json.dumps(resp.json()))


########################################################################################
###########                   API to Delete License Rule                  ##############
########################################################################################

def deleteLicenseRuleById(CINumber):

  #find licenseRuleID
  with open('licenseRulesCreatedInfo.txt', 'r') as FH:
      licenseRuleID=[val.split(':')[1] for val in FH.readlines() if CINumber in val][0]

  #print("LicenseRuleID:: ",licenseRuleID)

  endpoint="https://natwest.saas.appdynamics.com/controller/mds/v1/license/rules/{}".format(licenseRuleID)
  headers={'Authorization': 'Bearer {0}'.format(AccessToken)}

  #print("endpoint:: ",endpoint)
  #sys.exit()
  resp=requests.delete(endpoint, headers=headers)
  #resp=requests.get(endpoint, headers=headers)
  #print("Response Text: ",resp.text)

  #sys.exit()
  if resp.status_code != 204:
      print("Something went wrong while creating the License Rule")
      #raise ApiError('GET /controller/rest/applications/<ApplicationName> {}'.format(resp.status_code))
  else:
      print("License Rule successfully deleted for CINumber {}".format(CINumber))
      updateLicenseRuleFile(CINumber, delete=True)

########################################################################################
###########                   API to Create License Rule                  ##############
########################################################################################

def createLicenseRule(CINumber, ruleName):

  endpoint="https://natwest.saas.appdynamics.com/controller/mds/v1/license/rules"
  headers={'Authorization': 'Bearer {0}'.format(AccessToken), 'Content-Type': 'application/json'}

  #Setting up the payload. Updating values in the license_rule_template.txt file
  data=json.load(open(licenseRuleTemplateFile))

  config=ConfigParser.ConfigParser()
  config.optionxform = str #This is required so that ConfigParser doesn't change the keys to lowercase
  config.read('license.ini')
  licReference=CINumber+":LIC"
  license_types_dict={}

  for opt in config.options(licReference):
      license_types_dict["license_module_type"]=opt
      license_types_dict["number_of_licenses"]=config.getint(licReference, opt)
      data["entitlements"].append(copy.deepcopy(license_types_dict))

  #data["entitlements"].append(copy.deepcopy(license_types_dict))
  data["id"]=str(uuid.uuid4())
  data["name"]=ruleName
  data["description"]="License Rule for "+CINumber
  data["access_key"]=str(uuid.uuid4())

  #Creating Constraints
  constraintDict={}
  appConstraint='com.appdynamics.modules.apm.topology.impl.persistenceapi.model.ApplicationEntity'
  serverConstraint='com.appdynamics.modules.apm.topology.impl.persistenceapi.model.MachineEntity'
  match_string=ruleName.rsplit('_',1)[0]
  constraintDict={'entity_type_id': appConstraint, 'match_conditions': [{'attribute_type': 'NAME', 'match_type': 'STARTS_WITH', 'match_string': match_string}], 'constraint_type': 'ALLOW_SELECTED'}

  data['constraints'].append(copy.deepcopy(constraintDict))

  #print("Data for License Rule Creation :: ",data)
  #sys.exit()

  resp=requests.post(endpoint, headers=headers, json=data)
  #print("Response Text: ",resp.text)

  if resp.status_code != 200:
      print("Something went wrong while creating the License Rule")
      #raise ApiError('GET /controller/rest/applications/<ApplicationName> {}'.format(resp.status_code))
  else:
      respData=json.loads(resp.text)
      print("Access key for License rule against CINumber {} is : {}".format(CINumber, respData["access_key"]))
      updateLicenseRuleFile(respData)

## Write to File for License Rule Creation/Deletion ##

def updateLicenseRuleFile(data, delete=False):
  if(delete):
    with open('licenseRulesCreatedInfo.txt') as OF, open('licenseRulesCreatedInfo-updated.txt', 'w') as NF:
        for line in OF :
          if data not in line:
            NF.write(line)
    os.rename('licenseRulesCreatedInfo-updated.txt', 'licenseRulesCreatedInfo.txt')
  else:
    with open('licenseRulesCreatedInfo.txt', 'a') as WF:
        if WF.tell() == 0:
            WF.write("Name:id:access_key\n")

        WF.write('{0}:{1}:{2}\n'.format(data["name"],data["id"],data["access_key"]))

########################################################################################
###########            API to Create Role (From an existing Role)         ##############
########################################################################################

def createRoleFromTemplate(CINumber, TemplateRole):

  apps=getAppNamesByCI(CINumber)
  print("#### Creating {} Role for following Application(s) {} ### ".format(TemplateRole,apps))

  #TODO: Dashboard/Database of only specific App should be attached. Create Dashboard before assigning it to Role.

  endpoint="https://natwest.saas.appdynamics.com/controller/api/rbac/v1/roles"
  headers={'Authorization': 'Bearer {0}'.format(AccessToken), 'Content-Type': 'application/vnd.appd.cntrl+json;v=1'}

  #Fetching the template role from roleDumpFile
  roleDumpFile=TemplateRole+'.txt'
  with open(roleDumpFile, 'r') as infile:
      data=json.load(infile)

  permissions=data['permissions']

  del(data['id'])
  data['name']=CINumber+TemplateRole[:-12]    #TODO: New Role Name should follow conventions, have CI in it for example e..g CI0123456Config

  appPerms={}
  listOfPerms=[]

  for appId in apps.values():
      for perm in data["permissions"]:
          if perm["entityType"] == "APPLICATION":
              appPerms=copy.deepcopy(perm)
              appPerms["entityId"]=appId
              #del(appPerms["id"])
              listOfPerms.append(appPerms)

  #updating the permissions to only have non-APPLICATION permissions
  data["permissions"]=[perm for perm in data["permissions"] if perm["entityType"] != "APPLICATION"]

  data["permissions"].extend(listOfPerms)  #Appneding the permissions for CINumber specific apps to this Role

  for item in data["permissions"]:
      del(item["id"])

  #print("Updated Role Data :: ",data)

  #Updating the entityId for APPLICATION to this Application, Fetched in Step 1 i.e. appId.
  #print("Updated Data ::", json.dumps(data))
  #print("Headers :: ",headers)
  #print("endpint ::", endpoint)
  #sys.exit()

  resp=requests.post(endpoint, headers=headers, json=data)
  #print("Response Text: ",resp.text)

  #sys.exit()
  #TODO: Check if the new role is already created. Handle this Scenario.
  if resp.status_code != 200:
      print("Something went wrong")
      #raise ApiError('GET /controller/rest/applications/<ApplicationName> {}'.format(resp.status_code))

  #for item in resp.json():
  #    print('{} {} {}'.format(item[1], item[2], item[0]))

  #print(json.loads(resp.content.decode('utf-8')))


##################################################################################
## Delete Application ##
##################################################################################

def deleteApplication(CINumber):

  apps=getAppNamesByCI(CI)
  print("Appliations for {} are {}".format(CI, apps.values()))
  #sys.exit()
  endpoint="https://natwest.saas.appdynamics.com/controller/restui/allApplications/deleteApplication"
  headers={'Authorization': 'Bearer {0}'.format(AccessToken), 'Content-Type': 'application/json;charset=UTF-8'}

  for value in apps.values():
    params=value
    #print(type(params), params)
    resp=requests.post(endpoint, headers=headers, json=params)
    #print(resp.status_code)

    if resp.status_code != 204:
      print("Something went wrong in deleting Application {}".format(value))
      #raise ApiError('GET /controller/rest/applications/<ApplicationName> {}'.format(resp.status_code))
    else:
      print("Application {} deleted successfully\n".format(value))

##################################################################################
## Create Application ##
##################################################################################

def createApplication(CINumber):

  config=ConfigParser.ConfigParser()
  config.optionxform = str #This is required so that ConfigParser doesn't change the keys to lowercase
  config.read('license.ini')
  appReference=CINumber+":APP"

  endpoint="https://natwest.saas.appdynamics.com/controller/restui/allApplications/createApplication?applicationType=APM"
  headers={'Authorization': 'Bearer {0}'.format(AccessToken), 'Content-Type': 'application/json;charset=UTF-8'}

  name=config.get(appReference, 'NAME')
  area=config.get(appReference, 'AREA')
  envs=config.get(appReference, 'ENVS')
  brands=config.get(appReference, 'BRANDS')

  if not envs:
      print "Environments not provided, atleast one env is needed, e.g. DEV or PRD, Exitting......"
      sys.exit()

  envs=envs.split(',')
  brands=brands.split(',') if brands else brands
  appNames=[]

  for env in envs:
    if len(brands) > 0:
      for brand in brands:
        appName=area+"_"+name+"_"+brand+"_"+CINumber+"."+env
        appNames.append(appName)
    else:
      appName=area+"_"+name+"_"+CINumber+"."+env
      appNames.append(appName)

  #print("Applications to be created are ",appNames)

  for app in appNames:
    params={"name": app, "description": "Creating application {} for {}".format(app, CINumber)}
    resp=requests.post(endpoint, headers=headers, json=params)

    if resp.status_code != 200:
      print("Something went wrong in executeCreateApplicationAPI")
      #raise ApiError('GET /controller/rest/applications/<ApplicationName> {}'.format(resp.status_code))
    else:
      print("Application {} created successfully\n".format(app))


##################################################################################
## Download Package ##
##################################################################################

def downloadPackage(password, downloadURL):

  endpoint="https://identity.msrv.saas.appdynamics.com/v2.0/oauth/token"
  tokenData={"username": "sunil.aggarwal@rbs.com","password": password, "scopes": ["download"]}

  resp=requests.post(endpoint, json=tokenData)
  #print("Response Text: ",resp.text)

  respData=json.loads(resp.text)
  #print("Access Token:: ",respData['access_token'])
  accessToken=respData['access_token']

  endpoint=downloadURL
  headers={'Authorization': 'Bearer {0}'.format(AccessToken)}
  resp=requests.get(endpoint, headers=headers)
  if resp.status_code != 200:
      print("Something went wrong")
      #raise ApiError('GET /controller/rest/applications/<ApplicationName> {}'.format(resp.status_code))

  appDetails={item['name']:item['id'] for item in resp.json() if CINumber in item['name']}

  if appDetails:
    return appDetails
  else:
    print "No Matching Applications found"
    sys.exit()


##################################################################################
## Generate API Access Token ##
##################################################################################

def generateAccessToken():

  print("Generating Access Token for Authentication with API Client")
  endpoint="https://natwest.saas.appdynamics.com/controller/api/oauth/access_token"
  headers={'Content-Type': 'application/vnd.appd.cntrl+protobuf;v=1'}

  params={'grant_type':'client_credentials', 'client_id':'restAPIClient@natwest', 'client_secret':'fb835c17-853e-4000-8d87-73da2fed0a10'}
  #print("Params: ", params)
  resp=requests.post(endpoint, headers=headers, data=params)
  #print("Response Text: ",resp.text)

  respData=json.loads(resp.text)
  #print("Access Token:: ",respData['access_token'])
  return respData['access_token']


##################################################################################
## MAIN Section ##
##################################################################################

config=ConfigParser.ConfigParser()
config.read('defaults.ini')
#print(config.sections())

os.environ['https_proxy'] = config.get('proxy','https_proxy')

#TODO: Write a function to delete permission roles as well for clean-up
AccessToken=generateAccessToken()
#print("Access Token ::",AccessToken)

TemplateRoles=[config.get('templateRoles',opt) for opt in config.options('templateRoles')]
#print("TemplateRoles ::", TemplateRoles)

licenseRuleTemplateFile=config.get('files','licenseRuleTemplateFile')
#print("licenseRuleTemplateFile ::",licenseRuleTemplateFile)

parser = argparse.ArgumentParser()
parser.add_argument('--CINumber', nargs="*", required=True, help='CINumber for your Application')
args = parser.parse_args()
for CI in args.CINumber:
    #deleteApplication(CI)
    #sys.exit()
    createApplication(CI)
    print("CINumber :: ", CI)
    #deleteLicenseRuleById(CI)
    #sys.exit()
    data=getAppNamesByCI(CI)
    print("App Names ::",data)
    #licenseRuleName=data.keys()[0].rsplit('_',1)[0]+"_"+CI  #This will become something like DES_Demo_CI031390
    licenseRuleName='_'.join(data.keys()[0].split('_',2)[:2])+"_"+CI  #This will become something like DES_Demo
    print("LicenseRuleName ::",licenseRuleName)
    #sys.exit()
    createLicenseRule(CI, licenseRuleName)
    for templateRole in TemplateRoles:
        getRoleInfoByName(templateRole)
        createRoleFromTemplate(CI, templateRole)

#print(args.CINumber)
#sys.exit()
#data=getAppNamesByCI(CINumber)
#print(data)
#print(getAppIdByName())

#getRoleInfoByName()

#deleteLicenseRuleById(CI)