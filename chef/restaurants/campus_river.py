import re
import requests
import datetime

from .ocr import Ocr
from .scraping import Scraping
from .zomato import Zomato
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class CampusRiverO(Ocr):
    index = 'http://www.campusriver.cz/index.php/poledni-menu'

    def get_english_menu_url(self):
        r = requests.get(self.index)
        for link in BeautifulSoup(r.text, 'html.parser').find_all('img'):
                if '_b.jpg' in link['src'].lower():
                    return urljoin(self.index, link['src'])

    def is_vegetarian(self, meal, items):
        return items == 4, meal

    def filter_line(self, line):
        if line[0].isdigit() or line.lower().endswith('day'):
            return True, line
        return False, line

    def get(self):
        self.image_url_to_text(self.get_english_menu_url())
        filtered_text = self.filter_image_text()
        return filtered_text[datetime.datetime.today().isoweekday()]

class CampusRiverZ(Zomato):
    def __init__(self):
        self.zomato_id = 16507073

    def get(self):
        return super().get()[:5]

    def filter(self, meal):
        meal = re.sub('^[a-zA-Z0-9]\.', '', meal)  # menu number
        meal = re.sub('[0-9,]+(g|l)', '', meal)  # size
        meal = re.sub('[0-9]+,-', '', meal)  # price
        meal = re.sub('\(A[0-9-,]+\)', '', meal)  # allergens
        if meal.upper() == meal:  # title filter
            return None
        return meal

class CampusRiverS(Scraping):
    def __init__(self):
        self.regex = 'nabidka_1[^>]+(?:><i)?>[^\s]+([^<]+)'
        self.url = 'https://www.menicka.cz/3232-campus-river.html'
        self.encoding = 'windows-1250'

    def get(self):
        ret = []
        for i, food in enumerate(super().get()[:5]):
            ret.append((food, {'veg': i == 4})) # Last item is vegetarian
        return ret

class CampusRiver:
    @staticmethod
    def get():
        try:
            return CampusRiverO().get()
        except:
            try:
                return CampusRiverZ.get()
            except:
                return CampusRiverS.get()

if __name__ == '__main__':
    print(CampusRiver().get())
