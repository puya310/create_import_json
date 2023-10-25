import requests
import time
import json

#this script will output a JSON in the format that can be used with Snyk api-import-tool to import existing projects 

SNYK_TOKEN = "" #your snyk API token (account settings on snyk UI)
ORG_ID = "" #Org ID (this will need to be done/run for each org)
integrationId = "" #SCM integrationID (get from integration page) for integratino you want to import 
branch = "" #set the default branch to monitor (main/master, which is what Snyk monitors by default) 
fork = ""

#takes displayName attribute from target_url endpoint and feeds it into the import_url api
#considerations: branch 
target_url = f"https://api.snyk.io/rest/orgs/{ORG_ID}/targets?version=2023-10-13%7Ebeta&origin=github" #note this is set to origin: github , change if necessary 
import_url = f"https://api.snyk.io/v1/org/{ORG_ID}/integrations/{integrationId}/import"
branch_url = f"https://api.snyk.io/rest/orgs/{ORG_ID}/projects?origins=github&version=2023-10-13%7Ebeta" #wip 

all_targets = []

headers = {
    'Accept': 'application/vnd.api+json',
    'Authorization': f'token {SNYK_TOKEN}'
    }
res = requests.request("GET", target_url, headers=headers).json()

all_targets = res['data']
new_targets = []

    
for project in all_targets:
    # Extract project attributes - displayName output is in format of owner/name, so split them and assign to owner and name 
    attributes = project.get('attributes', {})
    display_name = attributes.get('displayName', '')
    print(display_name)
    split_name = display_name.split('/')

    if len(split_name) < 2:
        print(f"Invalid format for the repo: {display_name}")
        continue

    owner, name = split_name[:2]
  
    target = {
        "fork": fork,
        "name": name,
        "owner": owner,
        "branch": branch
    }
    request_data = {
        "target": target,
        "integrationId": integrationId,
        "orgId": ORG_ID
    }
    new_targets.append(request_data)

result_final = {
"targets": new_targets
}

with open('test1.json', 'w') as json_file:
    json.dump(result_final, json_file, indent=4)

print("Data saved to test1.json") 
   