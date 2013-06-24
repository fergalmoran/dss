import requests
from core.serialisers import json
from dss import localsettings

BASE_URL = localsettings.REALTIME_HOST
HEADERS = {
    'content-type': 'application/json'
}


def post_activity(activity_url):
    payload = {'message': activity_url}
    data = json.dumps(payload)
    r = requests.post(BASE_URL + '/api/activity', data=data, headers=HEADERS)
    if r.status_code == 200:
        return ""
    else:
        return r.text
