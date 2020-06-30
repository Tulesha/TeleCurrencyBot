import requests
from bs4 import BeautifulSoup
from collections import namedtuple

Rate = namedtuple('Rate', 'bank_name,name_currency,rate_buy,rate_sell')


# Парсер HTML страницы Myfin
def parser_HTML(currency_name: str, country_name: str):
    url = 'https://ru.myfin.by/currency'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    curr_url = url + f'/{currency_name}/{country_name}'

    source = requests.get(curr_url, headers=headers)
    main_text = source.text
    soup = BeautifulSoup(main_text, 'html.parser')

    convert = soup.find("tbody")

    return convert


def get_rate(country_name: str, currency_name: str):
    bank_list = list()
    info = parser_HTML(currency_name, country_name)
    info_odd = info.find_all('tr', {'class': 'row body tr-turn odd'})
    info_even = info.find_all('tr', {'class': 'row body tr-turn even'})

    for item in info_odd:
        bank_name = item.find('td', {'class': 'bank_name'}).text
        rates = item.find_all('td', {'class': currency_name.upper()})
        rate_buy = rates[0].text
        rate_sell = rates[1].text

        r = Rate(bank_name=bank_name, name_currency=currency_name.upper(), rate_buy=rate_buy, rate_sell=rate_sell)
        bank_list.append(r)

    for item in info_even:
        bank_name = item.find('td', {'class': 'bank_name'}).text
        rates = item.find_all('td', {'class': currency_name.upper()})
        rate_buy = rates[0].text
        rate_sell = rates[1].text

        r = Rate(bank_name=bank_name, name_currency=currency_name.upper(), rate_buy=rate_buy, rate_sell=rate_sell)
        bank_list.append(r)

    return bank_list


if __name__ == '__main__':
    for temp in get_rate('kazan', 'usd'):
        print(temp)
