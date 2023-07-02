import unittest
import os
from django.test import TestCase

from exchanger.utils.ex_mexc import ExMexc
from .test_base import TestBase


class TestExMexc(TestCase, TestBase):

    def setUp(self) -> None:
        super().setUp()
        self.host = 'https://api.mexc.com'
        self.url = 'account'
        self.prefix = '/api/v3/'
        self.api_key = os.environ.get('MEXC_API_KEY')
        self.api_secret = os.environ.get('MEXC_API_SECRET_KEY')
        self.exchanger = ExMexc(host=self.host,
                                url=self.url,
                                prefix=self.prefix,
                                api_key=self.api_key,
                                api_secret=self.api_secret)
        self.apiSecret_wrong = 'wrong'
        self.url_wrong = 'wrong'
        self.url_other = "myTrades"
        self.host_wrong = 'https://api.mexc.com/wrong'
        self.prefix_wrong = '/api/v1/'
        self.test_data_error = [{'error': 'currencies_account'}]
        self.test_data = {'accountType': 'SPOT',
                          'balances': [{'asset': "USDT", "free": '1', 'locked': '0'},
                                       {'asset': 'DOT', 'free': '1', 'locked': '2'},
                                       ],
                          'permissions': ['SPOT']
                          }

        self.api_key_wrong = None
        self.api_secret_wrong = None

    def test_gen_sign(self):
        result = self.exchanger.gen_sign()
        self.assertIn('timestamp', result)
        self.assertIn('signature', result)

    def test_get_request(self):
        result = self.exchanger._get_request().json()

        self.assertIsInstance(result, dict)
        self.assertIsNotNone(result['balances'])
        self.assertEqual(result['accountType'], 'SPOT')

    def test_get_request_with_wrong_apiSecret(self):
        self._set_wrong_api()
        result = self.exchanger._get_request().json()

        self.assertEqual(result['code'], 700002)
        self.assertEqual(result['msg'], 'Signature for this request is not valid.')

    def test_get_request_with_wrong_host(self):
        self._set_wrong_host()
        result = self.exchanger._get_request().json()

        self.assertEqual(result['code'], 404)
        self.assertEqual(result['msg'], 'Not Found')

    def test_get_request_with_wrong_prefix(self):
        self._set_wrong_prefix()
        result = self.exchanger._get_request().json()

        self.assertEqual(result['code'], 404)
        self.assertEqual(result['msg'], 'Not Found')

    def test_get_request_to_other_url(self):
        self._set_other_url()
        result = self.exchanger._get_request().json()

        self.assertEqual(result['code'], 700007)
        self.assertEqual(result['msg'], 'No permission to access the endpoint.')

    def test_get_request_with_wrong_url(self):
        self._set_wrong_url()
        result = self.exchanger._get_request()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.text, '')


if __name__ == '__main__':
    unittest.main(verbosity=1)
