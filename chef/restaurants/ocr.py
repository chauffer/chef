import requests
import re
import unicodedata
import contextlib
import io
import base64
import json


class Ocr:
    def __init__(self):
        self.session = requests.Session()
        self.text = None

    def image_url_to_text(self, url):
        r = self.session.get(url)
        image = io.BytesIO(r.content)
        data = {
            'image': {'content': base64.b64encode(image.getvalue()).decode('UTF-8')},
            'features': [{'type': 'DOCUMENT_TEXT_DETECTION', 'maxResults': 1}],
        }
        response = requests.post(
            'https://cxl-services.appspot.com/proxy',
            headers={'content-type': 'application/json; charset=UTF-8'},
            params={'url': 'https://vision.googleapis.com/v1/images:annotate'},
            data=json.dumps({'requests':[data]}),
        )
        self.text = response.json()['responses'][0]['textAnnotations'][0]['description']
        return self.text

    def filter_line(self, line):
        return True, line

    def is_vegetarian(self, meal, items):
        raise NotImplementedError

    def filter_image_text(self):
        day, menuitems = 0, {}

        for line in self.text_trash_removal():
            if len(line.split(' ')) == 1 and line.lower().endswith('day'):
                #1word == Monday, Tuesday, ..
                day += 1
                menuitems[day] = []
                continue
            if day == 0: # Still not at the days, skip.
                continue

            is_veg, line = self.is_vegetarian(line, len(menuitems[day]))

            menuitems[day].append((line.strip(), {'veg': is_veg}))
        return menuitems

    def text_trash_removal(self):
        if not self.text:
            raise 'bur'
        for line in self.text.split('\n'):
            if not line:
                continue

            is_line_allowed, line = self.filter_line(line)
            if not is_line_allowed:
                continue

            removal_regex = [
                '\([0-9,.]+\)',  # allergens
                '[0-9]+(?:\s?K.|\,?\-?)$',  # price
                '^\d?[\,\.]+\d*l?',  # restaurant n and liters
                '^\d+g',  # grams
            ]
            for regex in removal_regex:
                line = re.sub(regex, '', line).strip()
            if not line:
                continue

            yield line
