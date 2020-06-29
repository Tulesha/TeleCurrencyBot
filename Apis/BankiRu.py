import requests
from bs4 import BeautifulSoup
from collections import namedtuple

Rate = namedtuple('Rate', 'bank_name,name,rate')


# Замены запятой на точку, так как в html записана запятая, а это не валидные данные
def str_to_float(item: str):
    item = item.replace(',', '.')
    return float(item)


# Парсер HTML страницы
def parser_HTML():
    url = 'https://www.banki.ru/products/currency/cash/usd/moskva/'

    source = requests.get(url)
    main_text = source.text
    soup = BeautifulSoup(main_text)

    table = soup.find_all('div', {'class': 'table-flex__row item calculator-hover-icon__container'})

    return table


if __name__ == '__main__':
    print(parser_HTML())
