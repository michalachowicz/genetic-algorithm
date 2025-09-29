import json
from functions import cities, cities_chessboard, cities_groups

c = cities_groups(32, 4)
with open("cities_groups_30_3", "w")as file:
    json.dump(c, file)

