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
            for i, meal_info in enumerate(method().get(), start=1):

                if isinstance(meal_info, tuple):
                    meal, meal_data = meal_info[0], meal_info[1]
                else:
                    meal, meal_data = meal_info, {}

                meal = translate(meal).text

                if meal_data.get('veg', False):
                    meal = f'*{meal}*'

                if not meal_data.get('emoji'):
                    try:
                        r = requests.get(
                            'https://api.getdango.com/api/emoji',
                            params={'q': meal},
                            timeout=3,
                        )
                        meal_data['emoji'] = r.json()['results'][0]['text']
                    except:
                        meal_data['emoji'] = ':question:'

                fields.append(f"*{i}.* {meal_data['emoji']} {meal}")
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

        r = requests.post(settings.SLACK_WEBHOOK, json=slack_payload, timeout=5)
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
