from .campus_river import CampusRiver
from .big_sklizeno import BigSklizenoParser
from .small_sklizeno import SmallSklizeno
from .kiwi_bistro import KiwiBistro

restaurants = [
    ('Kiwi.com Bistro', KiwiBistro, {'color': '#1AAC98'}),
    ('Campus River', CampusRiver, {'color': '#022937'}),
    ('Big Sklizeno', BigSklizenoParser, {'color': '#FECE3A'}),
    ('Small Sklizeno', SmallSklizeno, {'color': '#B4BE42'}),
]
