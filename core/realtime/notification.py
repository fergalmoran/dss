import requests
import logging
import redis
from requests.packages.urllib3.exceptions import ConnectionError
from core.serialisers import json
from dss import localsettings
# TODO(fergal.moran@gmail.com): refactor these out to
# classes to avoid duplicating constants below
HEADERS = {
    'content-type': 'application/json'
}

logger = logging.getLogger('spa')


def post_notification(session_id, image, message):
    try:
        payload = {
            'sessionid': session_id,
            'image': image,
            'message': message
        }
        data = json.dumps(payload)
        r = requests.post(
            localsettings.REALTIME_HOST + 'notification',
            data=data,
            headers=HEADERS
        )
        if r.status_code == 200:
            return ""
        else:
            return r.text
    except ConnectionError:
        #should probably implement some sort of retry in here
        pass