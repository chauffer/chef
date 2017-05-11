import requests
import io

from google.cloud import vision


#tmp hardcoded cookies
headers={"cookie":"__inf_etc__=07d36902-30bb-4b12-a08e-183edb350ea5; forterToken=04123105931; __utma=96175366.2023676527.1466634696.1480537433.1490355071.3; __utmz=96175366.1490355071.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); rCookie=yg8mcyicjna97gk2yyacmbffnv94wg; _ga=GA1.2.2023676527.1466634696; ab_version=B; JSESSIONID=EB2237B25DFDD2B69F820695C3DEC7D8"}
menu_en="https://confluence.kiwi.com/download/attachments/12485782/9.5.-12.5.ENGL.jpg?version=1&modificationDate=1494313296287&api=v2&download=true"
menu_cz="https://confluence.kiwi.com/download/attachments/12485782/9.5.-12.5.CZ.jpg?version=1&modificationDate=1494336129429&api=v2&download=true"

def get_en_menu():
    r_en = requests.get(menu_en, headers=headers)
    return r_en.content

def get_cz_menu():
    r_cz = requests.get(menu_cz, headers=headers)
    return r_cz.content

def text_from_image(raw_image):
    vision_client = vision.Client()
    with io.BytesIO(raw_image) as image_file:
        content = image_file.read()
        image = vision_client.image(content=content)
    textz = image.detect_text()
    return textz[0].description


def decode_text(textz):
    print(textz)


def run():
    raw_image = get_en_menu()
    textz = text_from_image(raw_image)
    result = decode_text(textz)
    return result

