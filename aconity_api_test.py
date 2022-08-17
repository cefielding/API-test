import requests
import json
from datetime import datetime

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


    # Get API token
    api_token = response["authToken"]

    # Set headers for subsquent API requests
    headers["Cookie"] = f"XSRF-token={api_token}"
    headers["X-XSRF-token"] = api_token
    headers["Authorization"] = f"XSRF-token={api_token}"

    ######list of variables#####
    projectName = []          #1
    jobsName = []             #2
    jobsTime = []             #3
    velocity = []             #4
    factor = []               #4
    thickness = []            #4
    inputParam = []           #4
    power = []                #5
    speed = []                #5
    focus = []                #5
    laserParam = []           #5
    ############################

    # (1) Project name
    p = requests.get('http://172.16.17.240:9000/projects', headers= headers)
    projects = p.json()
    for data in projects:
        projectName.append(data['name'])
    #print(projectName)

    # (2) Name of job
    j = requests.get('http://172.16.17.240:9000/jobs', headers= headers) 
    jobs = j.json()
    for data in jobs:
        jobsName.append(data['name'])
    #print(jobsName)

    # (3) Timestamp of Job# --->requires = job_id
    l = requests.get('http://172.16.17.240:9000/jobs/62c2be634a0000c700fb287b', headers= headers)
    laser = l.json()
    for data in laser['history']:
        integer = int(data['timestamp'])/1000
        date = datetime.utcfromtimestamp(integer).strftime('%Y-%m-%d %H:%M:%S')
        jobsTime.append(date)
    #print(jobsTime)

    # (4) Input parameters# --->requires = job_id
    p = requests.get('http://172.16.17.240:9000/jobs/62c2be634a0000c700fb287b', headers= headers)
    parameters = p.json()
    for data in parameters['params']:
        if data['name']== 'deposition_velocity':
            velocity.append((data['name'],data['value'], data['unit']))
        elif data['name']== 'supply_factor':
            factor.append((data['name'],data['value'], data['unit']))
        elif data['name']== 'layer_thickness':
            thickness.append((data['name'],data['value'], data['unit']))
    inputParam.append((velocity, factor, thickness))
    #print(inputParam)


    # (5) Laser parameters#  --->requires = job_id
    s = requests.get('http://172.16.17.240:9000/jobs/62c2be634a0000c700fb287b', headers= headers) 
    Log = s.json()
    for data in Log['partRefs']:
        params = data['params']       
        for p in params:
            if p['name'] == 'laser_power':
                power.append((p['name'], p['value'], p['unit']))
            if p['name'] == 'mark_speed':
                speed.append((p['name'], p['value'], p['unit']))
            if p['name'] == 'defocus':
                focus.append((p['name'], p['value'], p['unit']))               
    laserParam.append((power[0], speed[0], focus[0]))
    print(laserParam)

    # -------- GETTING THE IDS -------- #
    #for i in sessions:
    #    newURL = ('http://172.16.17.240:9000/sessions/'+i)
    #    s1 = requests.get(newURL, headers= headers)  
    #    Log1 = s1.json()
    #    sessionID.append(Log1)
    #    for j in sessionID:
    #        for k in j:
    #            newURL = 'http://172.16.17.240:9000/sessions/'+i+'/configId/'+k
    #            s2 = requests.get(newURL, headers= headers)
    #            Log2 = s2.json()
    #            jobID.append(Log2)

    return projects



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
    # might need some async code after this to wait until the login has occurred
    # else it will try to request an API endpoint before it has recieved an
    # authentication token from the /login reponse
