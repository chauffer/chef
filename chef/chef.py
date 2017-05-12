#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import requests
from datetime import datetime, time

from . import settings

from .sklizeno import VelkeSklizeno


def dummy_chef():
    msg = "*Sklizeno*\n"
    msg += build_post_string(VelkeSklizeno().scrape().to_serializable())
    msg += "\n\n*Malé sklizeno*\n"
    msg += build_post_string({'main_dishes': [{'is_vege': False,
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
           {'is_vege': True,
            'name': 'Franfurtská polévka s párkem',
            'price': 29}]})
    r = requests.post(settings.SLACK_WEBHOOK,
                      json={
                          'text': msg,
                          'channel': settings.SLACK_CHANNEL,
                          'username': 'chef'
                      })
    print(r.status_code)
    print(r.content)


def build_post_string(restaurant):
    post_string = ""
    post_string += ":tada::tada::tada: Menu for date " + str(restaurant['menu_date']['date']) + " :tada::tada::tada:\n"
    post_string += build_food_string(restaurant['soups'])
    post_string += build_food_string(restaurant['main_dishes'])
    return post_string


def build_food_string(food_array):
    food_string = ""
    for food in food_array:
        food_string += pretty_formater(food['name'])
        food_string += " " + str(food['price']) + " czk"
        food_string += " :carrot:" if food['is_vege'] else ""
        food_string += "\n"
    return food_string


def pretty_formater(food_name):
    first_row = ""
    second_row = ""
    if len(food_name) > 80:
        for word in food_name.split(' '):
            if len(first_row) + len(word) < 80:
                first_row += word + " "
            else:
                second_row += word + " "
    else:
        first_row = food_name

    if len(second_row) == 0:
        for _ in range(int(80-len(first_row))):
            first_row += " "
    else:
        for _ in range(int(80-len(second_row))):
            second_row += " "

    if len(second_row) != 0:
        second_row = "\n" + second_row

    return first_row + second_row
