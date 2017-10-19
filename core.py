#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback

import requests

import settings
from small_sklizeno import SmallSklizeno
from big_sklizeno import BigSklizeno
from river import River


def le_chef():
    food_dict = {
        'channel': settings.SLACK_CHANNEL,
        'username': 'Chef',
        "icon_emoji": ":chef:",
        'attachments': [],
    }
    active_modules = [
        ("Malé sklizeno", SmallSklizeno(settings.ZOMATO_API_KEY)),
        ("Campus River", River(settings.ZOMATO_API_KEY)),
        ("Velké sklizeno", BigSklizeno())
    ]

    for restaurant_name, banana in active_modules:
        try:
            food_dict['attachments'] = [build_menu_json(restaurant_name, banana.get())]
        except Exception as fuck_something_went_wrong:
            traceback.print_exc()
            food_dict['attachments'] = [build_broken_json(restaurant_name)]

        from pprint import pprint
        pprint(food_dict)
        continue
        r = requests.post(settings.SLACK_WEBHOOK, json=food_dict)
        print(r.status_code)
        print(r.text)


def build_broken_json(restaurant_name):
    rest_json = {
        'title': f'{restaurant_name}',
        'color': '#36a64f',
        'footer': "Im broken, sry.",
        'fields': "This restaurant module broke, please fix it yourself because this isn't maintained project."
    }
    return rest_json


def build_menu_json(restaurant_name, menu_dict):
    rest_json = {
        'title': f'{restaurant_name}',
        'color': '#36a64f',
        'footer': f"Lunch is served from {menu_dict['start_date'].format('HH:mm')} until {menu_dict['end_date'].format('HH:mm')}",
        'fields': build_food_json(menu_dict['soups']) + build_food_json(menu_dict['dishes']),
    }
    return rest_json


def build_food_json(food_array):
    food_json = []
    for food in food_array:
        food_json.append({'value': food['name'].replace(u'\xa0', u' ') + (" :carrot:" if food.get('vege') else ""), 'short': 'true'})
        food_json.append({'value': f"{food['price']} Kč", 'short': 'true'})
    return food_json


if __name__=='__main__':
    le_chef()

