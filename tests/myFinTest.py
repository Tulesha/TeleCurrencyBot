import unittest

from apis.Myfin import parser_HTML
from apis.Myfin import Myfin
from apis.Myfin import MyFinBankError


class TestMyfinMethods(unittest.TestCase):
    def test_parser_HTML_is_not_None(self):
        self.assertIsNotNone(parser_HTML('usd', 'moskva'))

    def test_parser_HTML_error(self):
        with self.assertRaises(MyFinBankError):
            parser_HTML('fgvbhnjk', 'cfvgbhnjmk')

    def test_get_rate_usd_bank_name_type(self):
        bank_1 = Myfin('usd', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.bank_name, str))

    def test_get_rate_usd_rate_buy_type(self):
        bank_1 = Myfin('usd', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.rate_buy, float))

    def test_get_rate_usd_rate_sell_type(self):
        bank_1 = Myfin('usd', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.rate_sell, float))

    def test_get_rate_eur_bank_name_type(self):
        bank_1 = Myfin('eur', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.bank_name, str))

    def test_get_rate_eur_rate_buy_type(self):
        bank_1 = Myfin('eur', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.rate_buy, float))

    def test_get_rate_eur_rate_sell_type(self):
        bank_1 = Myfin('eur', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.rate_sell, float))

    def test_get_rate_gbp_bank_name_type(self):
        bank_1 = Myfin('gbp', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.bank_name, str))

    def test_get_rate_gbp_rate_buy_type(self):
        bank_1 = Myfin('gbp', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.rate_buy, float))

    def test_get_rate_gbp_rate_sell_type(self):
        bank_1 = Myfin('gbp', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.rate_sell, float))

    def test_get_rate_jpy_bank_name_type(self):
        bank_1 = Myfin('jpy', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.bank_name, str))

    def test_get_rate_jpy_rate_buy_type(self):
        bank_1 = Myfin('jpy', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.rate_buy, float))

    def test_get_rate_jpy_rate_sell_type(self):
        bank_1 = Myfin('jpy', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.rate_sell, float))

    def test_get_rate_cny_bank_name_type(self):
        bank_1 = Myfin('cny', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.bank_name, str))

    def test_get_rate_cny_rate_buy_type(self):
        bank_1 = Myfin('cny', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.rate_buy, float))

    def test_get_rate_cny_rate_sell_type(self):
        bank_1 = Myfin('cny', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.rate_sell, float))

    def test_myFin_constructor_error(self):
        with self.assertRaises(MyFinBankError):
            bank = Myfin('tvybuniomv', 'ctyvubioiuvyd6f7g')
