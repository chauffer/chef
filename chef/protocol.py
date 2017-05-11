class Soup():
    def __init__(self, name=None, price=None, is_vege=False):
        self.name = name
        self.price = int(price)
        self.is_vege = is_vege

    def to_serializable(self):
        return {
            'name': self.name,
            'price': self.price,
            'is_vege': self.is_vege
        }


class MainDish():
    def __init__(self, name=None, price=None, is_vege=False):
        self.name = name
        self.price = int(price)
        self.is_vege = is_vege

    def to_serializable(self):
        return {
            'name': self.name,
            'price': self.price,
            'is_vege': self.is_vege
        }


class ServingTime():
    def __init__(self, serving_times_raw=None, parsing_fun=None):
        self.time_from, self.time_to = parsing_fun(serving_times_raw)

    def to_serializable(self):
        return {
            'time_from': self.time_from,
            'time_to': self.time_to
        }


class Menu(object):
    def __init__(self, serving_time=None, soups=[], main_dishes=[], menu_date=None):
        self.menu_date = menu_date
        self.serving_time = serving_time
        self.soups = soups
        self.main_dishes = main_dishes

    def to_serializable(self):
        return {
            'menu_date': self.menu_date.to_serializable(),
            'serving_time': self.serving_time.to_serializable(),
            'soups': [s.to_serializable() for s in self.soups],
            'main_dishes': [md.to_serializable() for md in self.main_dishes],
        }

    def __str__(self):
        return self.to_serializable()


class MenuDate(object):
    def __init__(self, date_raw=None, parsing_fun=None):
        self.date = parsing_fun(date_raw)
        self.date_raw = date_raw

    def to_serializable(self):
        return {
            'date': self.date.isoformat()
        }
