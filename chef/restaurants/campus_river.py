from .zomato import Zomato
from .scraping import Scraping
import re

class CampusRiver(Zomato):
    def __init__(self):
        self.zomato_id = 16507073

    def get(self):
        return super().get()[:5]

    def filter(self, meal):
        meal = re.sub('^[a-zA-Z0-9]\.', '', meal)  # menu number
        meal = re.sub('[0-9,]+(g|l)', '', meal)  # size
        meal = re.sub('[0-9]+,-', '', meal)  # price
        meal = re.sub('\(A[0-9-,]+\)', '', meal)  # allergens
        if meal.upper() == meal:  # title filter
            return None
        return meal

class CampusRiver(Scraping):
    def __init__(self):
        self.regex = 'nabidka_1[^>]+(?:><i)?>[^\s]+([^<]+)'
        self.url = 'https://www.menicka.cz/3232-campus-river.html'
        self.encoding = 'windows-1250'

    def get(self):
        ret = []
        for i, food in enumerate(super().get()[:5]):
            ret.append((food, {'veg': i == 4})) # Last item is vegetarian
        return ret

if __name__ == '__main__':
    print(CampusRiver().get())
