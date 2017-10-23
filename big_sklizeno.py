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

dish_type = 0
dish_name = 1
dish_vege = 2
dish_price = 3

week_dish_name = 0
week_dish_price = 1

week_col_map = {
    week_dish_name: dish_name,
    week_dish_price: dish_price
}

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

        df = self.get_menu_table_df(today)

        out = self.process_df(df)
        return out

    def process_df(self, df):

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

        j = 0
        for nick, data in values.items():
            i = 0
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

                it = {
                    'name': nam,
                    'price': pric,
                    'vege': i == 3 or i == 4 or (i == 1 and j == 0),
                }
                i += 1
                out[nick.value].append(it)
                if i == 4:
                    break

            j += 1

        return out

    def get_menu_table_df(self, today):
        
        div_cls = 'large-6 medium-6 end columns'
        divs = self.soup.find_all('div', {'class': div_cls})

        today_str = today.format('DD.MM.YYYY')
        week_str = 'nab'
        headers = ['nab', 'dka', 'Pond', 'ter', 'eda', 'tvrtek', 'tek']
        
        today_div = None
        week_div = None

        # get today_div
        for div in divs:
            date_h2 = div.select_one('h2') #find('h2', {'class': 'nomargin nopading'})
            
            header = None
            if date_h2 is not None:
                if any((word in str(date_h2) for word in headers)):
                    header = date_h2.get_text()
               
            if header:
                if today_str in header:
                    today_div = div
                if week_str in header:
                    week_div = div

        cls_name = 'nabidka_4'
        p = HTMLTableParser()
        if today_div:
            li = today_div.find('table', {'class': cls_name})
            today_df = p.parse_html_table(li)
        
        pd.set_option("display.width",999)

        cls_name = 'nabidka_2'
        if week_div:
            li = week_div.find('table', {'class': cls_name})
            if li:
                week_df = p.parse_html_table(li)
            week_df.columns = [week_col_map[col] for col in week_df.columns]
            week_df[dish_type] = [self.get_dish_type(row) for row in week_df[dish_name]]

        week_df[dish_vege] = [0, 1, 1]

        today_df.drop(today_df.columns[[0, 1, 2, 3]], axis=1, inplace=True)
        frames = [today_df, week_df]
        all_df = pd.concat(frames, axis=0, ignore_index=True)

        return all_df

    def get_dish_type(self, txt):
        if 'Pol'.lower() in txt.lower():
            return 'Pol'
        else:
            return 'Menu'

if __name__ == '__main__':
    dict_ = BigSklizeno().get(today=arrow.utcnow().replace())
    print(dict_)
