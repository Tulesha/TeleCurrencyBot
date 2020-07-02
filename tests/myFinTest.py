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

    def test_get_rate_is_not_None(self):
        bank_1 = Myfin('usd', 'moskva')
        self.assertIsNotNone(bank_1.get_rate())

        bank_2 = Myfin('eur', 'moskva')
        self.assertIsNotNone(bank_2.get_rate())

        bank_3 = Myfin('gbp', 'moskva')
        self.assertIsNotNone(bank_3.get_rate())

        bank_4 = Myfin('jpy', 'moskva')
        self.assertIsNotNone(bank_4.get_rate())

        bank_5 = Myfin('cny', 'moskva')
        self.assertIsNotNone(bank_5.get_rate())

    def test_myFin_constructor_error(self):
        with self.assertRaises(MyFinBankError):
            bank = Myfin('tvybuniomv', 'ctyvubioiuvyd6f7g')
