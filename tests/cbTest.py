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

    def test_get_rates_usd_curr_name_1(self):
        bank_1 = CbBank(datetime.date(2002, 3, 2))
        usd = bank_1.get_rates_usd()
        self.assertEqual('USD', usd.name)

    def test_get_rates_usd_rate_1(self):
        bank_1 = CbBank(datetime.date(2002, 3, 2))
        usd = bank_1.get_rates_usd()
        self.assertEqual(30.9436, usd.rate)

    def test_get_rates_usd_curr_name_2(self):
        bank_2 = CbBank(datetime.date(2015, 7, 27))
        usd = bank_2.get_rates_usd()
        self.assertEqual('USD', usd.name)

    def test_get_rates_usd_rate_2(self):
        bank_2 = CbBank(datetime.date(2015, 7, 27))
        usd = bank_2.get_rates_usd()
        self.assertEqual(58.0374, usd.rate)

    def test_get_rates_usd_curr_name_3(self):
        bank_3 = CbBank(datetime.date(2020, 5, 30))
        usd = bank_3.get_rates_usd()
        self.assertEqual('USD', usd.name)

    def test_get_rates_usd_rate_3(self):
        bank_3 = CbBank(datetime.date(2020, 5, 30))
        usd = bank_3.get_rates_usd()
        self.assertEqual(70.7520, usd.rate)

    def test_get_rates_usd_error(self):
        bank_4 = CbBank(datetime.date(1950, 1, 27))
        with self.assertRaises(CentralBankError):
            bank_4.get_rates_usd()

    def test_get_rates_eur_curr_name_1(self):
        bank_1 = CbBank(datetime.date(2002, 3, 2))
        eur = bank_1.get_rates_eur()
        self.assertEqual('EUR', eur.name)

    def test_get_rates_eur_rate_1(self):
        bank_1 = CbBank(datetime.date(2002, 3, 2))
        eur = bank_1.get_rates_eur()
        self.assertEqual(26.8343, eur.rate)

    def test_get_rates_eur_curr_name_2(self):
        bank_2 = CbBank(datetime.date(2015, 7, 27))
        eur = bank_2.get_rates_eur()
        self.assertEqual('EUR', eur.name)

    def test_get_rates_eur_rate_2(self):
        bank_2 = CbBank(datetime.date(2015, 7, 27))
        eur = bank_2.get_rates_eur()
        self.assertEqual(63.6090, eur.rate)

    def test_get_rates_eur_curr_name_3(self):
        bank_3 = CbBank(datetime.date(2020, 5, 30))
        eur = bank_3.get_rates_eur()
        self.assertEqual('EUR', eur.name)

    def test_get_rates_eur_rate_3(self):
        bank_3 = CbBank(datetime.date(2020, 5, 30))
        eur = bank_3.get_rates_eur()
        self.assertEqual(78.5489, eur.rate)

    def test_get_rates_eur_error(self):
        bank_4 = CbBank(datetime.date(1950, 1, 27))
        with self.assertRaises(CentralBankError):
            bank_4.get_rates_eur()

    def test_get_rates_gbp_curr_name_1(self):
        bank_1 = CbBank(datetime.date(2002, 3, 2))
        gbp = bank_1.get_rates_gbp()
        self.assertEqual('GBP', gbp.name)

    def test_get_rates_gbp_rate_1(self):
        bank_1 = CbBank(datetime.date(2002, 3, 2))
        gbp = bank_1.get_rates_gbp()
        self.assertEqual(43.8254, gbp.rate)

    def test_get_rates_gbp_curr_name_2(self):
        bank_2 = CbBank(datetime.date(2015, 7, 27))
        gbp = bank_2.get_rates_gbp()
        self.assertEqual('GBP', gbp.name)

    def test_get_rates_gbp_rate_2(self):
        bank_2 = CbBank(datetime.date(2015, 7, 27))
        gbp = bank_2.get_rates_gbp()
        self.assertEqual(89.8825, gbp.rate)

    def test_get_rates_gbp_curr_name_3(self):
        bank_3 = CbBank(datetime.date(2020, 5, 30))
        gbp = bank_3.get_rates_gbp()
        self.assertEqual('GBP', gbp.name)

    def test_get_rates_gbp_rate_3(self):
        bank_3 = CbBank(datetime.date(2020, 5, 30))
        gbp = bank_3.get_rates_gbp()
        self.assertEqual(87.0603, gbp.rate)

    def test_get_rates_gbp_error(self):
        bank_4 = CbBank(datetime.date(1950, 1, 27))
        with self.assertRaises(CentralBankError):
            bank_4.get_rates_gbp()

    def test_get_rates_jpy_curr_name_1(self):
        bank_1 = CbBank(datetime.date(2002, 3, 2))
        jpy = bank_1.get_rates_jpy()
        self.assertEqual('JPY', jpy.name)

    def test_get_rates_jpy_rate_1(self):
        bank_1 = CbBank(datetime.date(2002, 3, 2))
        jpy = bank_1.get_rates_jpy()
        self.assertEqual(23.1527, jpy.rate)

    def test_get_rates_jpy_curr_name_2(self):
        bank_2 = CbBank(datetime.date(2015, 7, 27))
        jpy = bank_2.get_rates_jpy()
        self.assertEqual('JPY', jpy.name)

    def test_get_rates_jpy_rate_2(self):
        bank_2 = CbBank(datetime.date(2015, 7, 27))
        jpy = bank_2.get_rates_jpy()
        self.assertEqual(46.8044, jpy.rate)

    def test_get_rates_jpy_curr_name_3(self):
        bank_3 = CbBank(datetime.date(2020, 5, 30))
        jpy = bank_3.get_rates_jpy()
        self.assertEqual('JPY', jpy.name)

    def test_get_rates_jpy_rate_3(self):
        bank_3 = CbBank(datetime.date(2020, 5, 30))
        jpy = bank_3.get_rates_jpy()
        self.assertEqual(65.9539, jpy.rate)

    def test_get_rates_jpy_error(self):
        bank_4 = CbBank(datetime.date(1950, 1, 27))
        with self.assertRaises(CentralBankError):
            bank_4.get_rates_jpy()
