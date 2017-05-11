import math
import requests
from . import settings


def dummy_chef():
    msg = 'chef rulez'
    r = requests.post(settings.SLACK_WEBHOOK,
    json = {'text': msg,
            'channel':settings.SLACK_CHANNEL,
            'username': 'chef'})
    print(r.status_code)
    print(r.content)


def build_post_string(restaurant):
    post_string = ""
    post_string += build_food_string(restaurant['Soup'])
    post_string += build_food_string(restaurant['MainDish'])
    return post_string


def build_food_string(food_array):
    food_string = ""
    for food in food_array:
        food_string += pretty_formater(food['name'])
        food_string += " " + food['price']
        food_string += " :carrot:" if food['is_vege'] else ""
        food_string += "\n"
    return food_string


def pretty_formater(food_name, food_price):
    not_broken = True
    final_string = ""
    if len(food_name) > 80:
        for word in food_name.split(" "):
            if len(final_string) + len(word) > 80 and not_broken:
                final_string += "\n" + word
                not_broken = False
            else:
                final_string += word

    if len(final_string) + len(food_price) + 3 > 80:
        final_string += "\n"

    last_line = final_string.split("\n")
    num_of_t = int(math.ceil((80 - len(last_line[len(last_line) - 1])) / 4))
    for _ in range(num_of_t):
        final_string += "\t"
    return final_string
