import requests
import json

#response = requests.get('http://api.aconity3d.atlassian.net/')

#for data in response.json()['items']:
#    if data['answer_count'] ==0:
#        print(data['title'])
#        print(data['link'])
#    else:
#        print("skipped")
#    print()


r = requests.post('http://172.16.17.240:9000/login', data={'email':'admin@aconity3d.com', 'password':'passwd'})
response = r.json()
print(response)
#response = requests.get('http://172.16.17.240:9000/sessions')
#data = requests.get('http://172.16.17.240:9000/sessions')
#print('--->', data.json())

#response.json()

#for data in response.json():
#    print(data)
#    print()