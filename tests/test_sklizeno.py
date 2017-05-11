#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime, time, date

from sklizeno import MaleSklizeno
from protocol import Soup, MainDish, ServingTime, MenuDate


def test_serving_time():
    serving_time = ServingTime(time_from=time(11, 00), time_to=time(16, 00))
    assert serving_time.time_from, time(11, 00)
    assert serving_time.time_to, time(16, 00)


def test_soup():
    soup = Soup('Franfurtská polévka s párkem', 10.0, False)
    print soup.name, soup.price, soup.is_vege
    assert soup.name, 'Franfurtská polévka s párkem'
    assert soup.price, 10.0
    assert soup.is_vege, False

    soup = Soup()

    soup.name = 'Franfurtská polévka s párkem'
    soup.price = 10.0
    soup.is_vege = False

    assert soup.name, 'Franfurtská polévka s párkem'
    assert soup.price, 10.0
    assert soup.is_vege, False


def test_main_dish():
    main_dish = MainDish('Pečená kachna, medové zelí, domácí houskový knedlík', 100.0, False)

    assert main_dish.name, 'Pečená kachna, medové zelí, domácí houskový knedlík'
    assert main_dish.price, 100.0
    assert main_dish.is_vege, False

    main_dish = MainDish()

    main_dish.name = 'Pečená kachna, medové zelí, domácí houskový knedlík'
    main_dish.price = 100.0
    main_dish.is_vege = False

    assert main_dish.name, 'Pečená kachna, medové zelí, domácí houskový knedlík'
    assert main_dish.price, 100.0
    assert main_dish.is_vege, False


def test_date():
    male_sklizeno = MaleSklizeno()
    menu = male_sklizeno.scrape()
    assert datetime.now().date(), menu.menu_date.date


def test_currency():
    male_sklizeno = MaleSklizeno()
    menu = male_sklizeno.scrape()
    assert 'CZK', menu.currency


def test_soups():
    male_sklizeno = MaleSklizeno()
    menu = male_sklizeno.scrape()

    assert '29 Kč', menu.soups[0].price_raw
    assert 'Franfurtská polévka s párkem', menu.soups[0].name

    assert '29 Kč', menu.soups[1].price_raw
    assert 'Zeleninový vývar s nudlemi a zeleninou', menu.soups[1].name


def test_main_dishes():
    male_sklizeno = MaleSklizeno()
    menu = male_sklizeno.scrape()

    assert '129 Kč', menu.main_dishes[0].price_raw
    assert 'Pečená kachna, medové zelí, domácí houskový knedlík', menu.main_dishes[0].name

    assert '109 Kč', menu.main_dishes[1].price_raw
    assert 'Pečená kachna, medové zelí, domácí houskový knedlík', menu.main_dishes[1].name

    assert '109 Kč', menu.main_dishes[2].price_raw
    assert 'Dušená červená čočka, sázené vejce, kvásková bagetka', menu.main_dishes[2].name


def test_scraped_date():
    male_sklizeno = MaleSklizeno()
    menu = male_sklizeno.scrape()
    assert 'Thursday, 11 May (today)', menu.menu_date.date_raw


def parsing_function(data):
    return re.findall('.*?\(', data)[0]


def test_menu_date():
    menu_date = MenuDate(date_raw='Thursday, 11 May (today)', parsing_fun=parsing_function)
    assert menu_date.date, date(2017, 5, 11)
