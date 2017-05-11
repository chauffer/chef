
import requests
from . import settings

def dummy_chef():
    msg = 'chef rulez'
    r = requests.post('https://hooks.slack.com/services/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',
    json = {'text': msg,
            'channel':'#hack-days-chef',
            'username': 'chef'})
    print(r.status_code)
