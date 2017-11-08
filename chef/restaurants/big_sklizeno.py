from bs4 import BeautifulSoup

from .scraping import Scraping


class BigSklizeno(Scraping):
    def __init__(self):
        self.regex = '[^\n]3c3c3b.*;">([^<]+)<\/span'
        self.blacklist = ['Polévka I', 'Menu', 'Kč', 'cena']
        self.url = 'http://www.foodlovers.cz/index.php?pg=home'
        self.encoding = 'utf-8'


class BigSklizenoParser(Scraping):
    """Scraper using HTML parser instead of regex to find menu."""

    url = 'http://www.foodlovers.cz/index.php?pg=home'
    encoding = 'utf-8'
    soup = 'Polévka'
    meal = 'Menu'

    def get(self):
        bs = BeautifulSoup(self.get_content(), 'html.parser')
        table = bs.find('table', class_='nabidka_4')
        rows = table.find_all('tr')

        matches = []
        for row in rows:
            cols = row.find_all('td')
            if not cols:
                continue

            title = cols[0].text
            content = cols[1].text
            if self.soup in title:
                matches.append((content, {'emoji':'🍲'}))  # 🍜🥣🍲
            elif self.meal in title:
                matches.append((content, {'emoji':'🍛'}))
        return matches


if __name__ == '__main__':
    print(BigSklizenoParser().get())
