import requests
import os
import re
import base64
import io
import json
import datetime
from .ocr import Ocr

class KiwiBistro(Ocr):
    numbers = ('Soup 1', 'Soup 2', '1', '2', '3', '4')
    base_url, confluence_page_id = 'https://confluence.kiwi.com', 12485782

    def __init__(self):
        super().__init__()
        self.session.auth = (
            os.getenv('CHEF_CONFLUENCE_USER', 'simonebot'),
            os.getenv('CHEF_CONFLUENCE_PASS', ''),
        )

    def get_image_url(self):
        # Go to confluence page
        r = self.session.get(
            f'{self.base_url}/rest/api/content/{self.confluence_page_id}',
            params={'expand': 'body.view'},
        )
        content = r.json()['body']['view']['value']
        # Find & download image
        return self.base_url + re.findall(' src="(\/download[^"]+(?:EN|[^m]en)[^"]+)"', content)[0]

    def is_vegetarian(self, meal, items):
        meal_filtered = re.sub('^[^\s]*69[^\s]*|[^\s]*Veg[^\s]*', '', meal)
        is_veg = True if meal_filtered != meal else False
        return is_veg, meal_filtered

    def get(self):
        self.image_url_to_text(self.get_image_url())
        filtered_text = self.filter_image_text()
        return filtered_text[datetime.datetime.today().isoweekday()]

if __name__ == '__main__':
    print(KiwiBistro().get())
