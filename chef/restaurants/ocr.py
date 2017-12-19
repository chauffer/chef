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

    def filtered_image_text(self):
        if not self.text:
            raise 'bur'
        for line in self.text.split('\n'):
            line = re.sub('\([0-9,.]+\)', '', line) # allergens
            line = re.sub('[0-9]+\s?K.$', '', line) # price
            if len(line.strip()) == 0:
                continue

            yield line
