import requests
import logging
import redis
from core.serialisers import json
from dss import localsettings
# TODO(fergal.moran@gmail.com): refactor these out to
# classes to avoid duplicating constants below
HEADERS = {
    'content-type': 'application/json'
}

logger = logging.getLogger('spa')


def post_notification(user, message):
    try:
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('realtime', user.username + ': ' + message)
    except:
        logger.exception("Error posting redis notification")


def _post_notification(notification_url, session=None):
    payload = {'message': notification_url}

    if session:
        payload['session_id'] = session

    data = json.dumps(payload)
    r = requests.post(localsettings.REALTIME_HOST + '/api/notification',
                      data=data, headers=HEADERS)
    if r.status_code == 200:
        return ""
    else:
        return r.text
