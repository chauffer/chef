import re
import requests
import datetime

from .ocr import Ocr
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class CampusRiver(Ocr):
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


if __name__ == '__main__':
    print(CampusRiver().get())
