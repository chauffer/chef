from pprint import pprint as pp

import arrow
import requests


class SmallSklizeno(object):

    def __init__(self, api_key):
        super(SmallSklizeno, self).__init__()
        self.api_key = api_key

    def get(self):
        response = requests.get(
            'https://developers.zomato.com/api/v2.1/dailymenu?res_id=16507591',
            headers={'user_key': self.api_key},
            timeout=60
        ).json()

        if response.get('status') != 'success':
            return {}

        soups = []
        for i, soup in enumerate(response['daily_menus'][0]['daily_menu']['dishes'][:2]):
            soups.append({
                'name': soup['dish']['name'],
                'price': int(soup['dish']['price'].split('\xa0')[0]),
                'vege': i == 0,
            })

        dishes = []
        for i, dish in enumerate(response['daily_menus'][0]['daily_menu']['dishes'][2:5]):
            dishes.append({
                'name': dish['dish']['name'],
                'price': int(dish['dish']['price'].split('\xa0')[0]),
                'vege': i == 2,
            })

        daily_menu = {
            'start_date': arrow.get('1337-05-11T11:00'),
            'end_date': arrow.get('1337-05-11T16:00'),
            'soups': soups,
            'dishes': dishes
        }

        return daily_menu


if __name__ == '__main__':
    response = SmallSklizeno(api_key='PLACE-YOUR-SECRET-KEY-HERE').get()
    pp(response)
