import requests
import settings
import traceback
import datetime

from translate import translate
from restaurants import restaurants

def le_chef():
    slack_payload = {
        'channel': settings.SLACK_CHANNEL,
        'username': 'Chef V2',
        "icon_emoji": ":chef:",
        'attachments': [],
    }
    for name, method in restaurants:
        try:
            meal_number = 1
            fields = []
            for meal in method().get():
                meal = f'*{meal_number}.* {translate(meal).text}'
                fields.append(meal)
                meal_number += 1
            fields = [{'value': '\n'.join(fields)}]
        except:
            traceback.print_exc()
            fields = [{'value': 'Something broke.'}]
        
        slack_payload['attachments'] = [{
            'title': name,
            'fields': fields,
            'color': '#36a64f',
            'mrkdwn_in': ['fields'],
        }]

        r = requests.post(settings.SLACK_WEBHOOK, json=slack_payload)
        print(r)
        print(r.text)


def run_at_time():
    hour, minute = settings.TIME.split(':')
    notified_today = False
    while True:
        now = datetime.datetime.now()
        if now.hour == hour and now.minute == minute:
            le_chef()
            notified_today = True
        if notified_today and now.hour > hour:
            notified_today = False
        time.sleep(2)

if __name__=='__main__':
    le_chef()
    #run_at_time()

