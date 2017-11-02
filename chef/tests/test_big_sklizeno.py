from chef.restaurants.big_sklizeno import BigSklizenoParser
from pathlib import Path


class TestBigSklizeno(BigSklizenoParser):
    def get_content(self):
        with open(Path(__file__).parent / 'data' / 'big_sklizeno.html', 'r') as f:
            return ''.join(f.readlines())


def test_menu():
    results = TestBigSklizeno().get()

    assert len(results) == 7
    assert 'Hovězí vývar s domácími nudlemi a játrovou rýží' in results[0]
    assert 'Špagety s bazalkovým pestem sypané sýrem Gran Moravia' in results[-1]
