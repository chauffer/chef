import requests
import os
import re
import pyocr
import datetime
from PIL import Image

class KiwiBistro:

    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (
            os.getenv('CHEF_CONFLUENCE_USER', 'simonebot'),
            os.getenv('CHEF_CONFLUENCE_PASS', ''),
        )
        print(self.session.auth)
        self.base_url = 'https://confluence.kiwi.com'
        self.confluence_page_id = 12485782
    
    def _get_image_text(self):
        r = self.session.get(
            f'{self.base_url}/rest/api/content/{self.confluence_page_id}',
            params={'expand': 'body.view'},
        )
        content = r.json()['body']['view']['value']

        image = self.base_url + \
            re.findall(' src="(\/download[^"]+weekmenu_en[^"]+)"', content)[0]

        r = self.session.get(image, stream=True)

        tool = pyocr.get_available_tools()[0]
        return tool.image_to_string(
            Image.open(r.raw),
            lang='eng',
            builder=pyocr.builders.TextBuilder()
        )
    
    def _filter_image_text(self, text):
        day = 0
        menuitems = {}
        for line in text.split("\n"):
            if len(line.strip()) == 0:
                continue
            if len(line.split(" ")) == 1:
                day += 1
                menuitems[day] = []
                continue
            if day == 0:
                continue
            line = re.sub('\([0-9,.]+\)', '', line) # allergens
            line = re.sub('[0-9]+\s?K.$', '', line) # price
            is_veg = line
            line = re.sub('^[^\s]*69[^\s]*|[^\s]*Veg[^\s]*', '', line) # veg
            is_veg = True if is_veg != line else False
            line = line.strip()

            menuitems[day].append((line, {'veg': is_veg}))
        return menuitems

    def get(self):
        filtered_text = self._filter_image_text(self._get_image_text())
        return filtered_text[datetime.datetime.today().isoweekday()]

if __name__ == '__main__':
    print(KiwiBistro().get())
