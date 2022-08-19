from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
import requests
import json
from datetime import datetime
# ###################################################################################### #
# This bit of code can be used to obtain the job ids through sessions and configurations #
# ###################################################################################### #

login_details = {
    'rest_url':'http://172.16.17.240:9000/',
    'ws_url': 'ws://172.16.17.240:9000', 
    'email': 'admin@aconity3d.com',
    'password': 'passwd'
}

headers = { 'content-type': 'application/json' }

def login(details):
    payload = json.dumps({"email":details["email"], "password": details["password"]}) 
    r = requests.post('http://172.16.17.240:9000/login',payload, headers= headers)
    response = r.json()


    # Get API token to allow access
    api_token = response["authToken"]

    # Set headers for subsquent API requests
    headers["Cookie"] = f"XSRF-token={api_token}"
    headers["X-XSRF-token"] = api_token
    headers["Authorization"] = f"XSRF-token={api_token}"

    s = requests.get('http://172.16.17.240:9000/sessions', headers= headers) 
    sessions = s.json()
    for i in sessions:
        configlist = []
        newURL = ('http://172.16.17.240:9000/sessions/'+i)
        s1 = requests.get(newURL, headers= headers)  
        configs = s1.json()
        for name in configs:
            if "config_" in name:
                if not "none" in name:            
                    configlist.append(name) 
        
        #print(configlist)
        if len(configlist)>0:
            config_numbers =  [ d[7] for d in configlist ]
            sortedList = sorted(config_numbers)
            largest = sortedList[-1]
            index = [  d for d in configlist if "config_"+(largest) in d  ]
            newURL = ('http://172.16.17.240:9000/sessions/'+i+'/configId/'+index[0])
            s2 = requests.get(newURL, headers= headers)  
            jobids = s2.json()
            print("--->job ids", jobids)
            jobidList = []
            for name in jobids:
                if "job_" in name:
                    if not "none" in name:
                        jobidList.append(name)
            print(jobidList)
            print()

def api_request( endpoint ):
    # Endpoint is the URL you need to access ie "/sessions" or "/sessions/{sessionId}/configId/{conf_id}" etc.
    # Construct URL
    url = f"{login_details['url']}/{endpoint}"
    # Make GET request
    r.get( url, headers = headers )
    

    print(r.text()) # or use r.json()?

    return r.text()



if __name__ == "__main__":

    login(login_details)