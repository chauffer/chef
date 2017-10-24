from .scraping import Scraping

class BigSklizeno(Scraping):
    def __init__(self):
        self.regex = '[^\n]3c3c3b.*;">([^<]+)<\/span'
        self.blacklist = ['Polévka I', 'Menu', 'Kč', 'cena']
        self.url = 'http://www.foodlovers.cz/index.php?pg=home'
        self.encoding = 'utf-8'

if __name__ == '__main__':
    print(BigSklizeno().get())
