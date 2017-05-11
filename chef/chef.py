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
        food_string += food['name']
        food_string += " " + food['price']
        food_string += " :carrot:" if food['is_vege'] else ""
        food_string += "\n"
    return food_string
