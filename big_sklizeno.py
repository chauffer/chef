#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This setup is used"""
from __future__ import print_function

import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd

from enum import Enum
import arrow

import json


class ent(Enum):
    soup = 'soups'
    menu = 'dishes'


# markuj vege


class HTMLTableParser:

    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return [(table['id'],self.parse_html_table(table))\
                for table in soup.find_all('table')]

    def parse_html_table(self, table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)

        df = pd.DataFrame(columns = columns,
                          index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass

        return df


class BigSklizeno(object):
    url_main = 'http://www.foodlovers.cz/'
    url_obed = 'http://www.foodlovers.cz/index.php?pg=nabidka--obedy'

    def __init__(self):
        pass

    def get(self, today=None):
        """Get. you get it? IT does!"""

        if today is None:
            today = arrow.utcnow()

        out = {}
        menu = self.get_day_menu(today)
        out.update(menu)

        opening = self.get_opening(today)
        out.update(opening)

        return out

    def get_opening(self, today):
        """Returns.. hold it.. opening"""
        response = requests.get(self.url_obed)
        c = response.content

        out = {
            'start_date': arrow.get('1337-05-11T11:00'),
            'end_date': arrow.get('1337-05-11T15:00'),
        }
        return out

    def get_day_menu(self, today):
        """Returns some dict"""
        url = self.url_obed

        response = requests.get(self.url_obed)
        c = response.content
        self.soup = BeautifulSoup(c, 'html.parser')

        day_in_week = today.weekday() + 1
        if day_in_week in [6,7]:
            return dict()
        else:
            cnt = day_in_week

        df = self.get_menu_table_df(cnt)
        out = self.process_df(df)
        return out

    def process_df(self, df):

        dish_type = 0
        dish_name = 1
        dish_price = 3
        parts = {
            dish_type: {
                'Pol': ent.soup,
                'Menu': ent.menu,
            },
        }

        pd.set_option('expand_frame_repr', False)
        pd.set_option('max_colwidth', 70)

        df.index = df[dish_type]


        values = {}
        for column_name, column_parts in parts.items():
            for part_name, nick in column_parts.items():
                # get account
                trx = df[df[column_name].str.contains(part_name, na=False)]
                if not len(trx):
                    continue

                values[nick] = trx

        out = {
            mem: []
            for mem
            in ['soups', 'dishes']
        }

        for nick, data in values.items():
            for ind, row in data.iterrows():
                nam = row[dish_name]
                dirty_pric_str = row[dish_price]
                pric_str = ''
                for ch in dirty_pric_str:
                    if ch.isdigit():
                        pric_str += ch
                    else:
                        # when i get to som non digit- just break
                        break

                pric = int(pric_str)

                vegene = False

                it = {
                    'name': nam,
                    'price': pric,
                    'vege': vegene,
                }

                out[nick.value].append(it)


        return out

    def get_menu_table_df(self, cnt):

        cls_name = f'nabidka_{cnt}'
        li = self.soup.find('table', {'class': cls_name})

        p = HTMLTableParser()
        df = p.parse_html_table(li)
        return df

if __name__ == '__main__':
    dict_ = BigSklizeno().get(today=None)