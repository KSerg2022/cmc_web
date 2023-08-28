import unittest
import os
from django.test import TestCase

from binance.client import Client

from exchanger.utils.ex_binance import ExBinance
from .test_base import TestBase


class TestExBinance(unittest.TestCase, TestBase):

    def setUp(self) -> None:
        self.api_key = os.environ.get('BINANCE_API_KEY')
        self.api_secret = os.environ.get('BINANCE_API_SECRET_KEY')
        self.exchanger = ExBinance(api_key=self.api_key,
                                   api_secret=self.api_secret)

        self.host_wrong = 'https://api.binance.com/wrong/'
        self.api_key_wrong = 'wrong'
        self.api_secret_wrong = 'wrong'
        self.test_data_error = [{'error': 'spot_account'}, {'error': 'futures_coin_account'}]

        self.test_data_spot_account = [{'asset': 'BNB', 'free': '1.00000000', 'locked': '0.00000000'},
                                       {'asset': 'USDT', 'free': '5.00000000', 'locked': '10.00000000'}]
        self.test_data_futures_coin_account = [{'asset': 'ADA',
                                                'walletBalance': '695.38977160',
                                                'unrealizedProfit': '-256.44160411',
                                                'marginBalance': '438.94816749',
                                                'maintMargin': '11.39796832',
                                                'initialMargin': '455.91873296',
                                                'positionInitialMargin': '455.91873296',
                                                'openOrderInitialMargin': '0.00000000',
                                                'maxWithdrawAmount': '0.00001719',
                                                'crossWalletBalance': '0.00001719',
                                                'crossUnPnl': '0.00000000',
                                                'availableBalance': '0.00001719'}]

    def tearDown(self) -> None:
        del self.exchanger

    def _check_data(self, result):
        pass

    def test_get_futures_coin_account(self):
        result = self.exchanger.get_futures_coin_account()
        if not self._check_error_in_result_request(__class__, self.test_get_futures_coin_account, result):
            self.assertIsInstance(result, list)
            self.assertIsInstance(result[0], dict)
            self.assertIn('asset', result[0])
            self.assertIn('marginBalance', result[0])

    def test_get_futures_coin_account_with_wrong_api(self):
        self.exchanger.coin_m = Client(api_key=self.api_key_wrong,
                                       api_secret=self.exchanger.api_secret)
        result = self.exchanger.get_futures_coin_account()

        self.assertTrue(result['error'])
        self.assertIn('Check your "api key", "api secret"', result['error'])

    def test_get_futures_coin_account_with_wrong_secret(self):
        self.exchanger.coin_m = Client(api_key=self.exchanger.api_secret,
                                       api_secret=self.api_secret_wrong)
        result = self.exchanger.get_futures_coin_account()

        self.assertTrue(result['error'])
        self.assertIn('Check your "api key", "api secret"', result['error'])

    def test_get_spot_account(self):
        result = self.exchanger.get_spot_account()
        if not self._check_error_in_result_request(__class__, self.test_get_spot_account, result):
            self.assertIsInstance(result, list)
            self.assertIsInstance(result[0], dict)
            self.assertIn('asset', result[0])
            self.assertIn('free', result[0])
            self.assertIn('locked', result[0])

    def test_get_spot_account_with_wrong_api(self):
        self.exchanger.coin_m = Client(api_key=self.api_key_wrong,
                                       api_secret=self.exchanger.api_secret)
        result = self.exchanger.get_spot_account()

        self.assertTrue(result['error'])
        self.assertIn('Check your "api key", "api secret"', result['error'])

    def test_get_spot_account_with_wrong_secret(self):
        self.exchanger.coin_m = Client(api_key=self.exchanger.api_secret,
                                       api_secret=self.api_secret_wrong)
        result = self.exchanger.get_spot_account()

        self.assertTrue(result['error'])
        self.assertIn('Check your "api key", "api secret"', result['error'])

    def test_normalize_data(self):
        self._check_data_in_test_base(
            self.__class__,
            self.test_normalize_data,
            self.exchanger._normalize_data(self.test_data_spot_account,
                                           self.test_data_futures_coin_account)
        )

    def test_normalize_with_empty_data(self):
        result = self.exchanger._normalize_data(* self.test_data_error)

        self.assertIn(self.exchanger.exchanger, result)
        self.assertEqual(result[self.exchanger.exchanger], self.test_data_error)
