import requests
import logging
from bs4 import BeautifulSoup
from collections import namedtuple

Rate = namedtuple('Rate', 'bank_name,name_currency,rate_buy,rate_sell')


class ParserError(Exception):
    """Неизвестная ошибка при запросе API Myfin.ru"""


# Парсер HTML страницы Myfin
def parser_HTML(currency_name: str, country_name: str):
    url = 'https://ru.myfin.by/currency'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    curr_url = url + f'/{currency_name}/{country_name}'

    try:
        source = requests.get(curr_url, headers=headers)
        main_text = source.text
        soup = BeautifulSoup(main_text, 'html.parser')

        convert = soup.find("tbody")

        return convert
    except Exception:
        logging.exception("Parser error")
        raise ParserError


class Myfin:
    country_name = None
    currency_name = None
    bank_list = list()

    def __init__(self, country_name: str, currency_name: str):
        self.country_name = country_name
        self.currency_name = currency_name

    def get_rate(self):
        self.bank_list.clear()
        try:
            info = parser_HTML(self.currency_name, self.country_name)
            info_odd = info.find_all('tr', {'class': 'row body tr-turn odd'})
            info_even = info.find_all('tr', {'class': 'row body tr-turn even'})

            for item in info_odd:
                bank_name = item.find('td', {'class': 'bank_name'}).text
                rates = item.find_all('td', {'class': self.currency_name.upper()})
                rate_buy = rates[0].text
                rate_sell = rates[1].text

                r = Rate(bank_name=bank_name, name_currency=self.currency_name.upper(), rate_buy=rate_buy,
                         rate_sell=rate_sell)
                self.bank_list.append(r)

            for item in info_even:
                bank_name = item.find('td', {'class': 'bank_name'}).text
                rates = item.find_all('td', {'class': self.currency_name.upper()})
                rate_buy = rates[0].text
                rate_sell = rates[1].text

                r = Rate(bank_name=bank_name, name_currency=self.currency_name.upper(), rate_buy=rate_buy,
                         rate_sell=rate_sell)
                self.bank_list.append(r)

            return self.bank_list

        except Exception:
            logging.exception('Invalid attribute')
            raise AttributeError
