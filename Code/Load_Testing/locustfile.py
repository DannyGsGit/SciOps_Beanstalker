### To run this swarm, execute the following command from the locustfile.py directory:
### locust --host=http://your.api.domain.com/

from locust import HttpLocust, TaskSet
import json
#headers = {'content-type': 'application/json'}
#r = l.client.post("/post/endpoint", data=json.dumps(payload), headers=headers, catch_response=True)



from locust import HttpLocust, TaskSet

url = "/rideshare"
payload =json.dumps({'weathersit':1, 'weekday':3, 'atemp':0.8, 'hum':0.1, 'windspeed':0.20})


def makecall(l):
    l.client.post(url, payload)


class UserBehavior(TaskSet):
    tasks = {makecall: 1}
