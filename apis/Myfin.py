import http

import requests
from bs4 import BeautifulSoup
from collections import namedtuple

Rate = namedtuple('Rate', 'bank_name,rate_buy,rate_sell')


class MyFinBankError(Exception):
    """Неизвестная ошибка при запросе API Myfin.ru"""


def parser_HTML(currency_name: str, city_name: str):
    """
    Метод парсит html страницу, чтобы достать данные о банках
    :param currency_name: название валюты
    :param city_name: название города
    :return: возвращает данные о банках
    :raise MyFinBankError: выбрасывается тогда, когда нам не удалось получить данные
    """
    url = 'https://ru.myfin.by/currency'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    curr_url = url + f'/{currency_name}/{city_name}'

    source = requests.get(curr_url, headers=headers)
    if source.status_code != http.HTTPStatus.OK:
        raise MyFinBankError('Bad status code')

    main_text = source.text
    soup = BeautifulSoup(main_text, 'html.parser')

    convert = soup.find("tbody")

    return convert


class Myfin:
    """
    Используется, чтобы доставать данные о банках из Myfin.ru
    """
    __city_name = None
    __currency_name = None
    __info = None

    def __init__(self, currency_name: str, city_name: str):
        """
        Конструктор
        :param currency_name: название валюты
        :param city_name: название города
        """
        self.__city_name = city_name
        self.__currency_name = currency_name
        self.__info = parser_HTML(self.__currency_name, self.__city_name)

    def get_rate(self):
        """
        Метод получения определенной валюты в городе сайта Myfin.ru
        :return: возвращает данные по курсу валюты в определенном городе
        :raise MyFinBankError: выбрасывается тогда, когда нам не удалось получить данные
        """
        bank_list = list()
        try:
            info_odd = self.__info.find_all('tr', {'class': 'row body tr-turn odd'})
            info_even = self.__info.find_all('tr', {'class': 'row body tr-turn even'})

            for item in info_odd:
                bank_name = item.find('td', {'class': 'bank_name'}).text
                rates = item.find_all('td', {'class': self.__currency_name.upper()})
                rate_buy = rates[0].text
                rate_sell = rates[1].text

                r = Rate(bank_name=bank_name, rate_buy=rate_buy,
                         rate_sell=rate_sell)
                bank_list.append(r)

            for item in info_even:
                bank_name = item.find('td', {'class': 'bank_name'}).text
                rates = item.find_all('td', {'class': self.__currency_name.upper()})
                rate_buy = rates[0].text
                rate_sell = rates[1].text

                r = Rate(bank_name=bank_name, rate_buy=rate_buy,
                         rate_sell=rate_sell)
                bank_list.append(r)

            return bank_list

        except AttributeError:
            raise MyFinBankError
