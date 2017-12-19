import requests
import os
import re
import base64
import io
import json
import datetime
from .ocr import Ocr

class KiwiBistro(Ocr):

    def __init__(self):
        super().__init__()
        self.session.auth = (
            os.getenv('CHEF_CONFLUENCE_USER', 'simonebot'),
            os.getenv('CHEF_CONFLUENCE_PASS', ''),
        )

        self.base_url = 'https://confluence.kiwi.com'
        self.confluence_page_id = 12485782

    def get_image_url(self):
        # Go to confluence page
        r = self.session.get(
            f'{self.base_url}/rest/api/content/{self.confluence_page_id}',
            params={'expand': 'body.view'},
        )
        content = r.json()['body']['view']['value']
        # Find & download image
        return self.base_url + re.findall(' src="(\/download[^"]+weekmenu_en[^"]+)"', content)[0]

    def _filter_image_text(self):
        day, menuitems = 0, {}

        for line in self.filtered_image_text():
            if len(line.split(" ")) == 1: #1word == Monday, Tuesday, ..
                day += 1
                menuitems[day] = []
                continue
            if day == 0: # Still not at the days, skip.
                continue

            is_veg = line
            line = re.sub('^[^\s]*69[^\s]*|[^\s]*Veg[^\s]*', '', line) # veg
            is_veg = True if is_veg != line else False
            line = line.strip()

            menuitems[day].append((line, {'veg': is_veg}))
        return menuitems

    def get(self):
        self.image_url_to_text(self.get_image_url())
        filtered_text = self._filter_image_text()
        return filtered_text[datetime.datetime.today().isoweekday()]

if __name__ == '__main__':
    print(KiwiBistro().get())
