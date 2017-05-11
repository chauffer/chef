#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import lxml.html as html
from datetime import datetime, time
from pprint import pprint as pp

from protocol import Soup, MainDish, Menu, MenuDate, ServingTime


class MetaFood(object):
    def __init__(self):
        pass


class Zomato(MetaFood):
    BASE_URL = 'https://www.zomato.com/'
    restaurants = {
        'male_sklizeno': 'brno/sklizeno-foodie-market-bohunice-brno-jihozápad/daily-menu'
    }

    def __init__(self):
        super(Zomato, self).__init__()


class FoodLovers(MetaFood):
    BASE_URL = 'http://www.foodlovers.cz/'
    restaurants = {
        'velke_sklizeno': 'index.php?pg=home'
    }


class Restaurant(object):
    def __init__(self):
        pass


class MaleSklizeno(Restaurant):
    name = 'Malé sklizeno'
    code = 'male_sklizeno'

    items_indexes = [
        (0, MenuDate),
        (1, Soup),
        (2, Soup),
        (3, MainDish),
        (4, MainDish),
        (5, MainDish)
    ]

    def __init__(self):
        self.zomato = Zomato()
        self.menu = Menu()

    def scrape(self):

        def parsing_function(data):
            return re.findall('.*?\(', data)[0]

        self.response = requests.get('{0}{1}'.format(self.meta.BASE_URL, self.meta.restaurants[self.code]))
        items = html.cssselect('#menu-preview > div.tmi-groups > div:nth-child(1)')
        for i, item in enumerate(items):
            for index in self.items_indexes:
                if i == index:
                    self.menu.menu_date = MenuDate(date_raw=item.text.replace('\n', '').strip(),
                                                   parsing_fun=parsing_function)


class VelkeSklizeno(Restaurant):
    name = 'Velké sklizeno'
    code = 'velke_sklizeno'

    items_indexes = [
        (1, Soup),
        (2, Soup),
        (3, MainDish),
        (4, MainDish),
        (5, MainDish),
        (6, MainDish),
        (7, MainDish),
    ]

    def __init__(self):
        self.meta = FoodLovers()
        self.menu = Menu()

    def scrape(self):

        def menu_date_parsing_function(data):
            return datetime.strptime(''.join(data.split()[3:]), '%d.%m.%Y').date()

        def serving_time_parsing_function(data):
            times = re.findall('[0-9]{2}.[0-9]{2}', data)
            return (time(int(times[0].split('.')[0]),
                         int(times[0].split('.')[1])),
                    time(int(times[1].split('.')[0]),
                         int(times[1].split('.')[1])))

        self.response = requests.get('{0}{1}'.format(self.meta.BASE_URL, self.meta.restaurants[self.code]))
        tree = html.fromstring(self.response.content)
        items = tree.cssselect('body > div.row-wide.homepage > div > div.large-6.medium-6.large-offset-1.columns > table > tbody > tr')
        for i, item in enumerate(items):
            for index in self.items_indexes:
                if i == index[0] and index[1] == Soup:
                    try:
                        name = item.cssselect('td:nth-child(2) > font > span')[0].text
                    except:
                        name = item.cssselect('td:nth-child(2)')[0].text

                    try:
                        price = item.cssselect('td:nth-child(4) > font > span')[0].text.split(' ')[0]
                    except:
                        price = item.cssselect('td:nth-child(4)')[0].text.split(' ')[0]

                    self.menu.soups.append(Soup(name=name,
                                                price=price,
                                                is_vege=i == 2))
                elif i == index[0] and index[1] == MainDish:
                    print item.cssselect('td:nth-child(2)')[0].text, "HHUHUH"
                    print html.tostring(item)
                    try:
                        name = item.cssselect('td:nth-child(2) > font > span')[0].text
                    except:
                        name = item.cssselect('td:nth-child(2)')[0].text

                    try:
                        price = item.cssselect('td:nth-child(4) > font > span')[0].text.split(' ')[0]
                    except:
                        price = item.cssselect('td:nth-child(4)')[0].text.split(' ')[0]

                    self.menu.main_dishes.append(MainDish(name=name,
                                                          price=price,
                                                          is_vege=i > 5))

        date_raw = tree.cssselect('body > div.row-wide.homepage > div > div.large-6.medium-6.large-offset-1.columns > h3')[0].text
        self.menu.menu_date = MenuDate(date_raw=date_raw, parsing_fun=menu_date_parsing_function)
        serving_times_raw = tree.cssselect('body > div.row.homepage-top > div:nth-child(2) > div > div:nth-child(2) > p > strong')[0].text
        self.menu.serving_time = ServingTime(serving_times_raw=serving_times_raw, parsing_fun=serving_time_parsing_function)
        return self.menu


pp(VelkeSklizeno().scrape().to_serializable())
