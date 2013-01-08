import os
DEBUG = True
if os.name == 'posix':
    DSS_TEMP_PATH = "/tmp/"
    DSS_LAME_PATH = "lame"
    DSS_WAVE_PATH = "waveformgen"
else:
    DSS_TEMP_PATH = "d:\\temp\\"
    DSS_LAME_PATH = "D:\\Apps\\lame\\lame.exe"
    DSS_WAVE_PATH = "d:\\Apps\\waveformgen.exe"

DATABASE_NAME = 'deepsouthsounds'
DATABASE_USER = 'root'
DATABASE_PASSWORD = ''
#DATABASE_HOST  = ''

PIPELINE_YUI_BINARY = ""
FACEBOOK_APP_SECRET = ''

JS_SETTINGS = {
    'CHAT_HOST'             : "ext-test.deepsouthsounds.com:8081",
    'API_URL'               : "/api/v1/",
    'LIVE_STREAM_URL'       : "radio.deepsouthsounds.com",
    'LIVE_STREAM_PORT'      : "8000",
    'LIVE_STREAM_MOUNT'     : "mp3",
    'DEFAULT_AUDIO_VOLUME'  : "1",
    'SM_DEBUG_MODE'         : False,
    'LIVE_STREAM_INFO_URL'  : "radio.deepsouthsounds.com:8000/mp3"
}
"""
WAVEFORM_URL  = 'http://waveforms.podnoms.com/'
IMAGE_URL     = 'http://images.podnoms.com/'
STATIC_URL    = 'http://static.podnoms.com/'
"""
IMAGE_URL = 'http://ext-test.deepsouthsounds.com:8000/media/'
GOOGLE_ANALYTICS_CODE = ''
SENDFILE_BACKEND = 'sendfile.backends.development'
#SENDFILE_BACKEND = 'sendfile.backends.xsendfile'
#SENDFILE_BACKEND = 'sendfile.backends.nginx'

