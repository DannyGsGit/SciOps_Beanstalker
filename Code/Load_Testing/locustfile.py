### To run this swarm, execute the following command from the locustfile.py directory:
### locust --host=http://your.api.domain.com/

from locust import HttpLocust, TaskSet
import json

url = "/rideshare"
payload =json.dumps({'weathersit':1, 'weekday':3, 'atemp':0.8, 'hum':0.1, 'windspeed':0.20})


def makecall(l):
    l.client.post(url, payload)


class UserBehavior(TaskSet):
    tasks = {makecall: 1}


### Start the Locust UI on port :8089 of the machine running this script.
