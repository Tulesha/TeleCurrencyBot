import datetime

import http
import xmltodict
import requests
from collections import namedtuple

Rate = namedtuple('Rate', 'name,rate')


class CentralBankError(Exception):
    """Неизвестная ошибка при запросе API CB"""


def parser_cb_xml(date_now: datetime.date):
    """
    Метод, который достает информацию по курсам валют из xml Центробанка и превращает в json
    :param date_now: дата, по которой нужно получить курс
    :return: возращает json файл
    :raise CentralBankError: выбрасывается когда у нас плохой xml или плохой статус код
    """
    get_curl = 'http://www.cbr.ru/scripts/XML_daily.asp'
    date_format = "%d/%m/%Y"
    params = {
        "date_req": date_now.strftime(date_format)
    }

    r = requests.get(get_curl, params=params)
    if r.status_code != http.HTTPStatus.OK:
        raise CentralBankError('Bad status code')
    resp = r.text

    try:
        data = xmltodict.parse(resp)
        return data
    except xmltodict.expat.error:
        raise CentralBankError('Bad xml')


def str_to_float(item: str):
    """Метод который заменяет запятую в строке на точку. Нужен, потому что ЦБ выдает данные с запятой

    """
    item = item.replace(',', '.')
    return float(item)


class CbBank:
    """
    Используется чтобы доставать данные по валютам из ЦБ
    """
    __info = None

    def __init__(self, date_now: datetime.date):
        """
        Конструктор
        :param date_now: дата, по которой нужно получить курс
        """
        self.__info = parser_cb_xml(date_now)

    def get_rates_usd(self):
        """
        Получить информацию по курсу доллара
        :return: возвращает данные по курсу доллара
        :raise CentralBankError: выбрасывается когда у нас плохой xml или плохой статус код
        """
        section_id = 'R01235'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    r = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return r
            return None

        except (KeyError, TypeError, ValueError):
            raise CentralBankError('Json traversal error')

    def get_rates_eur(self):
        """
        Получить информацию по курсу евро
        :return: возвращает данные по курсу евро
        :raise CentralBankError: выбрасывается когда у нас плохой xml или плохой статус код
        """
        section_id = 'R01239'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    r = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return r
            return None

        except (KeyError, TypeError, ValueError):
            raise CentralBankError('Json traversal error')

    def get_rates_gbp(self):
        """
        Получить информацию по курсу фунту
        :return: возвращает данные по курсу фунта
        :raise CentralBankError: выбрасывается когда у нас плохой xml или плохой статус код
        """
        section_id = 'R01035'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    r = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return r
            return None
        except (KeyError, TypeError, ValueError):
            raise CentralBankError('Json traversal error')

    def get_rates_jpy(self):
        """
        Получить информацию по курсу иена
        :return: возвращает данные по курсу иена
        :raise CentralBankError: выбрасывается когда у нас плохой xml или плохой статус код
        """
        section_id = 'R01820'
        try:
            for item in self.__info['ValCurs']['Valute']:
                if item['@ID'] == section_id:
                    r = Rate(
                        name=item['CharCode'],
                        rate=str_to_float(item['Value'])
                    )
                    return r
            return None
        except (KeyError, TypeError, ValueError):
            raise CentralBankError('Json traversal error')
