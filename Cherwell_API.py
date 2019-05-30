#Cherwell REST api test.
#client key: 915ca6e9-7319-4fec-bc9a-8ca62fb68efa
#url: http://servicedeskonline.sdiad.simedarbyindustrial.com/CherwellAPI/api/V1/getsearchitems

import requests
import json

#api details
clientId = '915ca6e9-7319-4fec-bc9a-8ca62fb68efa'
serverName = "servicedeskonline.sdiad.simedarbyindustrial.com"
baseUri = "http://" + serverName + "/CherwellAPI/"
tokenUri = baseUri + "token"
authMode = "Internal"

tokenReqBody = {
    "Accept": "application/json",
    "grant_type": "password",
    "client_id": clientId,
    "username": "csdapi",
    "password": "Dq9clse3"
}

#Rec IDs
#Incident ID
incidentBusObjId = '6dd53665c0c24cab86870a21cf6434ae'
#Survey Element ID's
surveyBusObjId   = '93e5787a6fbc8e475c0f464e248c193a1f1cc1704c'
surveyResponseBusObjID = '93e57897b3b548cd7cc165443e861042062f25aee7'
surveyQuestionBusObjId = '93e5776e57d4913d8b915f47e8b7999a1a9192d19a'

#secures connection the rest api by creating a session.
def secureAccess():
    tokenReqBody = {
        "Accept": "text/json",
        "grant_type": "password",
        "client_id": clientId,
        #"username": input("Please enter username: "),
        #"password": input("Please enter password: ")
        #update later to manual password
        "username": "admin_harodav",
        "password": "Xdq5pe3L"
    }
    accessToken = requests.post(url = tokenUri, data = tokenReqBody, json=True)
    #authMode = "Internal"
    myRefreshToken = accessToken.json()['refresh_token']
    myResAccessToken =  "Bearer " +  accessToken.json()["access_token"]
    myRequestHeader = {"Authorization": myResAccessToken}

    return {
        "token": accessToken,
        "refresh_token": myRefreshToken,
        "resAccessToken": myResAccessToken,
        "requestHeader": myRequestHeader
    }

#using the refresh token update the current token 
def refreshAccessToken(oldToken):
    refreshReqBody = {
        "Accept": "application/json",
        "grant_type": "refresh_token",
        "client_id": clientId,
        "refresh_token": oldToken['refresh_token']
    }

    newToken = requests.post(url = tokenUri, data = refreshReqBody, json = True)

    newRefreshToken = newToken.json()['refresh_token']
    newResAccessToken =  "Bearer " +  newToken.json()["access_token"]
    newRequestHeader = {"Authorization": newResAccessToken}
    return {
        "token": newToken,
        "refresh_token": newRefreshToken,
        "resAccessToken": newResAccessToken,
        "requestHeader": newRequestHeader
    }

#requests a template of a business object by parsing the business object id and the current session token.
def GetBusObjTemplate(busObjId, token):
    surveyTemplateUri = baseUri + "api/V1/getbusinessobjecttemplate"
    reqBody = {
        "busObId": busObjId,
        "includeRequired": True,
        "includeAll": True,
        "fieldNames": [
            "string"
        ]
        }
    return requests.post(url = surveyTemplateUri, data = reqBody, headers = token['requestHeader'], json = True)

#update template object by passing itself, the field to be updated and the new value.
def UpdateTemplate(template, changeList):
    #objTemplate  = json.loads(jsonTemplate.text)
    #create index to assist passing field name to an index in field list.
    idxLookup = CreateFieldIndex(template)
    for field in changeList:
        template['fields'][idxLookup[field['field']]]['value'] = field['value']
        template['fields'][idxLookup[field['field']]]['dirty'] = True
    #return updated template
    return template

#returns a dict of fields and the corresponding index from the template list of fields
def CreateFieldIndex(template):
    idxLookup = {}
    idx = 0
    for field in template['fields']:
        idxLookup[field['name']] = idx
        idx += 1
    
    return idxLookup

def CreateNewBusObj(template, busObj, token):
    createUri = baseUri + 'api/V1/savebusinessobject'
    reqBody = {
        "busObId": busObj,
        "fields": template["fields"]
        }

    reqJson = json.dumps(reqBody)
    
    #add content type to header. Not sure why application/json wasn't working...
    token['requestHeader']['Content-Type'] = 'text/json'
    requests.post(createUri, data = reqJson, headers = token['requestHeader'], json=True)
    #refreshing the access token will clear the Content-Type setting above    

#open a session.
accessToken = secureAccess()
print(accessToken['refresh_token'])

#refresh the session.
accessToken = refreshAccessToken(accessToken)
print(accessToken['refresh_token'])

#request a template
#incidentTemplate =  GetBusObjTemplate(incidentBusObjId, accessToken)

sprintactivtyID = '9423e7ce3fb0ae0599715141f89d9a33281b47d288'
saTemplate = GetBusObjTemplate(sprintactivtyID, accessToken)
saTemplate = json.loads(saTemplate.text)


fieldChanges = [
    {"field": "SprintActivity", "value": "SPRINT TEST 2"},
    {"field": "SprintActivityID", "value": "1"},
    {"field": "StartDate", "value": "2019-05-28"},
    {"field": "SprintTeam", "value": "Service Desk Level 1"},
]

saTemplate = UpdateTemplate(saTemplate, fieldChanges)
CreateNewBusObj(saTemplate, sprintactivtyID, accessToken)

#this will clear Content-Type
accessToken =refreshAccessToken(accessToken)
print("*")


#---------------------------------------------------------
# Things to do:
#---------------------------------------------------------
#
# Investigate why text/json needs to be used rather than
# application/json
#
#
#---------------------------------------------------------

#saTemplate = UpdateTemplate(saTemplate, "SprintActivity", "SPRINT TEST 1")
#saTemplate = UpdateTemplate(saTemplate, "SprintActivityID", "1")
#aTemplate = UpdateTemplate(saTemplate, "StartDate", "2019-05-28")
#saTemplate = UpdateTemplate(saTemplate, "SprintTeam", "Service Desk Level 1")

#update template object by passing itself, the field to be updated and the new value.
#def UpdateTemplate(template, field, value):
#    #objTemplate  = json.loads(jsonTemplate.text)
#    #create index to assist passing field name to an index in field list.
#    idxLookup = CreateFieldIndex(template)
#    #update field value and the dirty setting (commits change on post request).
#    template['fields'][idxLookup[field]]['value'] = value
#    template['fields'][idxLookup[field]]['dirty'] = True
#    #return updated template
#    return template
