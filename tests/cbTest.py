import unittest
import random
import datetime

from apis.cbBank import parser_cb_xml
from apis.cbBank import str_to_float
from apis.cbBank import CbBank
from apis.cbBank import CentralBankError


class TestCbMethods(unittest.TestCase):
    def test_parser_cb_xml_is_not_none(self):
        self.assertIsNotNone(parser_cb_xml(datetime.date(2002, 3, 2)))

    def test_str_to_float(self):
        number = random.random()
        self.assertEqual(number, str_to_float(f'{number}'))

    def test_get_rates_usd(self):
        bank_1 = CbBank(datetime.date(2002, 3, 2))
        usd = bank_1.get_rates_usd()
        self.assertEqual('USD', usd.name)
        self.assertEqual(30.9436, usd.rate)

        bank_2 = CbBank(datetime.date(2015, 7, 27))
        usd = bank_2.get_rates_usd()
        self.assertEqual('USD', usd.name)
        self.assertEqual(58.0374, usd.rate)

        bank_3 = CbBank(datetime.date(2020, 5, 30))
        usd = bank_3.get_rates_usd()
        self.assertEqual('USD', usd.name)
        self.assertEqual(70.7520, usd.rate)

        bank_4 = CbBank(datetime.date(1950, 1, 27))
        with self.assertRaises(CentralBankError):
            bank_4.get_rates_usd()

    def test_get_rates_eur(self):
        bank = CbBank(datetime.date(2002, 3, 2))
        eur = bank.get_rates_eur()
        self.assertEqual('EUR', eur.name)
        self.assertEqual(26.8343, eur.rate)

        bank_2 = CbBank(datetime.date(2015, 7, 27))
        eur = bank_2.get_rates_eur()
        self.assertEqual('EUR', eur.name)
        self.assertEqual(63.6090, eur.rate)

        bank_3 = CbBank(datetime.date(2020, 5, 30))
        eur = bank_3.get_rates_eur()
        self.assertEqual('EUR', eur.name)
        self.assertEqual(78.5489, eur.rate)

        bank_4 = CbBank(datetime.date(1950, 1, 27))
        with self.assertRaises(CentralBankError):
            bank_4.get_rates_eur()

    def test_get_rates_gbp(self):
        bank = CbBank(datetime.date(2002, 3, 2))
        gbp = bank.get_rates_gbp()
        self.assertEqual('GBP', gbp.name)
        self.assertEqual(43.8254, gbp.rate)

        bank_2 = CbBank(datetime.date(2015, 7, 27))
        gbp = bank_2.get_rates_gbp()
        self.assertEqual('GBP', gbp.name)
        self.assertEqual(89.8825, gbp.rate)

        bank_3 = CbBank(datetime.date(2020, 5, 30))
        gbp = bank_3.get_rates_gbp()
        self.assertEqual('GBP', gbp.name)
        self.assertEqual(87.0603, gbp.rate)

        bank_4 = CbBank(datetime.date(1950, 1, 27))
        with self.assertRaises(CentralBankError):
            bank_4.get_rates_gbp()

    def test_get_rates_jpy(self):
        bank = CbBank(datetime.date(2002, 3, 2))
        jpy = bank.get_rates_jpy()
        self.assertEqual('JPY', jpy.name)
        self.assertEqual(23.1527, jpy.rate)

        bank_2 = CbBank(datetime.date(2015, 7, 27))
        jpy = bank_2.get_rates_jpy()
        self.assertEqual('JPY', jpy.name)
        self.assertEqual(46.8044, jpy.rate)

        bank_3 = CbBank(datetime.date(2020, 5, 30))
        jpy = bank_3.get_rates_jpy()
        self.assertEqual('JPY', jpy.name)
        self.assertEqual(65.9539, jpy.rate)

        bank_4 = CbBank(datetime.date(1950, 1, 27))
        with self.assertRaises(CentralBankError):
            bank_4.get_rates_jpy()
