import requests
from core.serialisers import json
from dss import localsettings, settings


def post_activity(activity_url):
    payload = {'message': activity_url}
    data = json.dumps(payload)
    r = requests.post(localsettings.REALTIME_HOST + '/api/activity', data=data, headers=settings.REALTIME_HEADERS)
    if r.status_code == 200:
        return ""
    else:
        return r.text
