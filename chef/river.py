import io
import os
import requests

from google.cloud import vision


def image_from_url(url):
    result = requests.get(url)
    if result.status_code != 200:
        raise ConnectionError()
    return result.content

def text_from_image(raw_image):
    vision_client = vision.Client()
    with io.BytesIO(raw_image) as image_file:
        content = image_file.read()
        image = vision_client.image(content=content)
    textz = image.detect_text()
    return textz[0].description

def decode(menu):
    for l in menu.splitlines():
        print(l)

def run():
    raw_image = image_from_url('http://www.campusriver.cz/images/19.tyden_free_2017b.jpg')
    textz = text_from_image(raw_image)
    decode(textz)


if __name__ == '__main__':
    run()
