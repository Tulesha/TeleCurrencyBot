import json

filename_city = 'cities.json'
with open(filename_city) as fl:
    cities = json.load(fl)

filename_curr = 'currencies.json'
with open(filename_curr) as fr:
    currencies = json.load(fr)
