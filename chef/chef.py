#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from datetime import time

from . import settings

from .sklizeno import VelkeSklizeno


def dummy_chef():
    food_dict = {
        'channel': settings.SLACK_CHANNEL,
        'username': 'chef',
        'attachments': []
    }
    temp_rest_data = {'main_dishes': [{'is_vege': False,
                                       'name': 'Pečená kachna, medové zelí, domácí houskový knedlík',
                                       'price': 129},
                                      {'is_vege': False,
                                       'name': 'Vepřové nudličky s rajčaty a paprikou, rýže basmati',
                                       'price': 109},
                                      {'is_vege': True,
                                       'name': 'Dušená červená čočka, sázené vejce, kvásková bagetka',
                                       'price': 109}],
                      'menu_date': {'date': '2017-05-12'},
                      'serving_time': {'time_from': time(11, 0),
                                       'time_to': time(16, 0)},
                      'soups': [{'is_vege': True,
                                 'name': 'Zeleninový vývar s nudlemi a zeleninou',
                                 'price': 29},
                                {'is_vege': False,
                                 'name': 'Franfurtská polévka s párkem',
                                 'price': 29}]}
    food_dict['attachments'].append(build_rest_json("Sklizeno :tada::tada::tada:",
                                                      VelkeSklizeno().scrape().to_serializable()))
    food_dict['attachments'].append(build_rest_json("Malé sklizeno :tada::tada::tada:", temp_rest_data))

    r = requests.post(settings.SLACK_WEBHOOK,
                      json=food_dict)
    print(r.status_code)
    print(r.content)


def build_rest_json(rest_name, restaurant):
    rest_json = {
        'pretext': rest_name,
        'color': '#36a64f',
        'footer': "Menu for date " + str(restaurant['menu_date']['date']),
        'fields': build_food_json(restaurant['soups']) + build_food_json(restaurant['main_dishes'])
    }
    return rest_json


def build_food_json(food_array):
    food_json = []
    for food in food_array:
        food_json.append({'value': food['name'] + (" :carrot:" if food['is_vege'] else ""), 'short': 'true'})
        food_json.append({'value': str(food['price']) + " czk", 'short': 'true'})
    return food_json
