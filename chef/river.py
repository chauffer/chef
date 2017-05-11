import io
import os
import requests
import re

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

def get_soup(meal_str):
    m = re.findall('[\d,]+l ([\w ,]+)', meal_str)
    return m[:-1]

def get_meals(meal_str):
    m = re.findall('\d\. [\d]+g (.+?) (\d+)', meal_str, flags=re.DOTALL)
    return m

def decode(menu):
    soups = get_soup(menu)
    meals = get_meals(menu)
    print(soups)
    print(meals)


def run():
    raw_image = image_from_url('http://www.campusriver.cz/images/19.tyden_free_2017b.jpg')
    textz = text_from_image(raw_image)
    decode(textz)


if __name__ == '__main__':
    run()
