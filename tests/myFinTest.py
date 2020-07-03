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

    def test_get_rate_type(self):
        bank_1 = Myfin('usd', 'moskva')
        for bank in bank_1.get_rate():
            self.assertTrue(isinstance(bank.bank_name, str))
            self.assertTrue(isinstance(bank.rate_buy, float))
            self.assertTrue(isinstance(bank.rate_sell, float))

        bank_2 = Myfin('eur', 'moskva')
        for bank in bank_2.get_rate():
            self.assertTrue(isinstance(bank.bank_name, str))
            self.assertTrue(isinstance(bank.rate_buy, float))
            self.assertTrue(isinstance(bank.rate_sell, float))

        bank_3 = Myfin('gbp', 'moskva')
        for bank in bank_3.get_rate():
            self.assertTrue(isinstance(bank.bank_name, str))
            self.assertTrue(isinstance(bank.rate_buy, float))
            self.assertTrue(isinstance(bank.rate_sell, float))

        bank_4 = Myfin('jpy', 'moskva')
        for bank in bank_4.get_rate():
            self.assertTrue(isinstance(bank.bank_name, str))
            self.assertTrue(isinstance(bank.rate_buy, float))
            self.assertTrue(isinstance(bank.rate_sell, float))

        bank_5 = Myfin('cny', 'moskva')
        for bank in bank_5.get_rate():
            self.assertTrue(isinstance(bank.bank_name, str))
            self.assertTrue(isinstance(bank.rate_buy, float))
            self.assertTrue(isinstance(bank.rate_sell, float))

    def test_myFin_constructor_error(self):
        with self.assertRaises(MyFinBankError):
            bank = Myfin('tvybuniomv', 'ctyvubioiuvyd6f7g')
