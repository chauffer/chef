#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import requests
from datetime import datetime

from . import settings

from .sklizeno import VelkeSklizeno


def dummy_chef():
    msg = build_post_string(VelkeSklizeno().scrape().to_serializable())
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
 'serving_time': {'time_from': datetime.time(11, 0),
                  'time_to': datetime.time(16, 0)},
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
        food_string += food['name']
        food_string += " " + str(food['price']) + " czk"
        food_string += " :carrot:" if food['is_vege'] else ""
        food_string += "\n"
    return food_string


def pretty_formater(food_name, food_price):
    broken = False
    final_string = ""
    if len(food_name) > 80:
        for word in food_name.split(" "):
            if len(final_string) + len(word) > 80 and broken:
                final_string += "\n" + word
                broken = True
            else:
                final_string += word

    if len(final_string) + len(str(food_price)) + 3 > 80:
        final_string += "\n"

    last_line = final_string.split("\n")
    num_of_t = int(math.ceil((80 - len(last_line[len(last_line) - 1])) / 4))
    for _ in range(num_of_t):
        final_string += "\t"
    return final_string
