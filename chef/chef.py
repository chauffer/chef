
import requests
from . import settings

def dummy_chef():
    msg = 'chef rulez'
    r = requests.post(settings.SLACK_WEBHOOK,
    json = {'text': msg,
            'channel':settings.SLACK_CHANNEL,
            'username': 'chef'})
    print(r.status_code)
    print(r.content)
