from .zomato import Zomato

class SmallSklizeno(Zomato):
    def __init__(self):
        self.zomato_id = 16507591

    def get(self):
        return super().get()[:5]

    def is_vegetarian(self, meal, number):
        return (number in (0, 4))
if __name__ == '__main__':
    print(SmallSklizeno().get())
