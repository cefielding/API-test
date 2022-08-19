from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
import requests
import json
from datetime import datetime
import numpy as np

# ###################################################################################### #
# The following code gives you all job details such as timestamp, parameters and project #
# so long as you have the job id in the first place                                      #
# ###################################################################################### #

login_details = {
    'rest_url':'http://172.16.17.240:9000/',
    'ws_url': 'ws://172.16.17.240:9000', 
    'email': 'admin@aconity3d.com',
    'password': 'passwd'
}

headers = { 'content-type': 'application/json' }

def login(details):
    # Allows access into the acoities database
    payload = json.dumps({"email":details["email"], "password": details["password"]}) 
    r = requests.post('http://172.16.17.240:9000/login',payload, headers= headers)
    response = r.json()

    # Get API token to allow access
    api_token = response["authToken"]

    # Set headers for subsquent API requests
    headers["Cookie"] = f"XSRF-token={api_token}"
    headers["X-XSRF-token"] = api_token
    headers["Authorization"] = f"XSRF-token={api_token}"

    ######list of variables#####
    projectName = []          #1
    jobsName = []             #2
    jobID = []                #3
    TimeStamp = []            #3           
    jobsTime = []             #4
    velocity = []             #5
    factor = []               #5
    thickness = []            #5
    inputParam = []           #5
    power = []                #6
    speed = []                #6
    focus = []                #6
    laserParam = []           #6
    ############################

    # (1) Job Project name
    p = requests.get('http://172.16.17.240:9000/jobs/62c2be634a0000c700fb287b', headers= headers)
    projects = p.json()
    projName = projects['projectName']
    print(projName)  
    #print(projectName)


    # (2) Name of job
    j = requests.get('http://172.16.17.240:9000/jobs', headers= headers) 
    jobs = j.json()
    for data in jobs:
        jobsName.append(data['name'])
    #print(jobsName)

    # (3) job ID
    j = requests.get('http://172.16.17.240:9000/jobs', headers= headers) 
    jobs = j.json()
    for data in jobs:
        idArray = data['_id']
        for key, value in idArray.items():
            # gets list together of all ids
            jobID.append(value)

            newURL = ('http://172.16.17.240:9000/jobs/'+value)
            s1 = requests.get(newURL, headers= headers)  
            idInfo = s1.json()

            for data in idInfo['history']:
                Time = data['timestamp']
            # gets list of all timestamping dates
            TimeStamp.append(Time)
    # gets a list of the position of largest value to smallest
    indexList = np.argsort(-np.array(TimeStamp))
    SortedJobs = []
    for data in indexList:
        # sorts jobs into a list of highest to lowest according to most recent
        SortedJobs.append(jobID[data])


    # (4) Timestamp of Job --->requires = job_id
    t = requests.get('http://172.16.17.240:9000/jobs/62c2be634a0000c700fb287b', headers= headers)
    time = t.json()
    for data in time['history']:
        # divide y 1000 to convert from miliseconds
        integer = int(data['timestamp'])/1000
        #formats the timestamp into a readable form
        date = datetime.utcfromtimestamp(integer).strftime('%Y-%m-%d %H:%M:%S')
        jobsTime.append(date)
    #print(jobsTime)

    # (5) Input parameters --->requires = job_id
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


    # (6) Laser parameters  --->requires = job_id
    l = requests.get('http://172.16.17.240:9000/jobs/62c2be634a0000c700fb287b', headers= headers) 
    laser = l.json()
    for data in laser['partRefs']:
        params = data['params']       
        for p in params:
            if p['name'] == 'laser_power':
                power.append((p['name'], p['value'], p['unit']))
            if p['name'] == 'mark_speed':
                speed.append((p['name'], p['value'], p['unit']))
            if p['name'] == 'defocus':
                focus.append((p['name'], p['value'], p['unit']))     
    # takes the 0 position as there are two copies of each data entry          
    laserParam.append((power[0], speed[0], focus[0]))
    #print(laserParam)

    return projects



if __name__ == "__main__":

    login(login_details)
    # might need some async code after this to wait until the login has occurred
    # else it will try to request an API endpoint before it has recieved an
    # authentication token from the /login reponse
