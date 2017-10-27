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
    for name, method, custom_data in restaurants:
        try:
            fields = []
            menu_items = method().get()
            for meal_number, menu_item in enumerate(menu_items, start=1):
                if isinstance(menu_item, tuple):
                    meal, meal_type = menu_item
                else:
                    meal, meal_type = menu_item, ''

                meal = f'*{meal_number}.* {meal_type} {translate(meal).text}'
                fields.append(meal)
            fields = [{'value': '\n'.join(fields)}]
        except:
            traceback.print_exc()
            fields = [{'value': 'Something broke.'}]
        
        slack_payload['attachments'] = [{
            'title': name,
            'fields': fields,
            'color': custom_data.get('color', '#36a64f'),
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

