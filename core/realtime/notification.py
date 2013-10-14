import requests
from core.serialisers import json
from dss import localsettings
# TODO(fergal.moran@gmail.com): refactor these out to classes to avoid duplicating constants below
HEADERS = {
    'content-type': 'application/json'
}


def post_notification(notification_url, session=None):
    payload = {'message': notification_url}

    if session:
        payload['session_id'] = session

    data = json.dumps(payload)
    r = requests.post(localsettings.REALTIME_HOST + '/api/notification', data=data, headers=HEADERS)
    if r.status_code == 200:
        return ""
    else:
        return r.text
