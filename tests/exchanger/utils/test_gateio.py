import unittest
import os
from django.test import TestCase
import time

from exchanger.utils.ex_gateio import ExGate
from .test_base import TestBase


class TestExGate(TestCase, TestBase):

    def setUp(self) -> None:
        super().setUp()
        self.host = 'https://api.gateio.ws'
        self.prefix = '/api/v4'
        self.api_key = os.environ.get('GATE_API_KEY')
        self.api_secret = os.environ.get('GATE_API_SECRET_KEY')
        self.exchanger = ExGate(host=self.host,
                                prefix=self.prefix,
                                api_key=self.api_key,
                                api_secret=self.api_secret)
        self.url = '/spot/accounts'

        self.api_key_wrong = 'wrong'
        self.api_secret_wrong = 'wrong'

        self.url_wrong = '/spot/wrong'
        self.host_wrong = 'https://api.gateio.ws/wrong'
        self.prefix_wrong = '/api/v1/'
        self.test_data_error = [{'error': 'currencies_account'}]
        self.test_data = [{'currency': 'FIRO', 'available': '5', 'locked': '0'},
                          {'currency': 'POLS', 'available': '10', 'locked': '5'}
                          ]
        self.apiSecret_wrong = None
        self.url_other = None

    def tearDown(self) -> None:
        del self.exchanger

    def _get_error_404(self, data):
        result = self.exchanger._get_request(data)

        self.assertEqual(result.status_code, 404)

    def test_gen_sign(self):
        result = self.exchanger.gen_sign('GET',
                                         self.exchanger.host + self.url,
                                         self.exchanger.query_param)

        self.assertIn('KEY', result)
        self.assertIn('Timestamp', result)
        self.assertIn('SIGN', result)

    def test_get_total_balance(self):
        result = self.exchanger.get_total_balance().json()

        self.assertIsInstance(result, dict)
        self.assertIn('details', result.keys())
        self.assertIn('spot', list(result.values())[0])
        self.assertIn('total', result.keys())

    def test_get_request(self):
        result = self.exchanger._get_request(self.url).json()

        self.assertIsInstance(result, list)
        self.assertNotEqual(len(result), 0)
        self.assertIn('currency', result[0])
        self.assertIn('available', result[0])
        self.assertIn('locked', result[0])

    def test_get_request_with_wrong_key(self):
        self._set_wrong_api()
        result = self.exchanger._get_request(self.url).json()

        self.assertEqual(result['message'], 'Invalid key provided')
        self.assertEqual(result['label'], 'INVALID_KEY')

    def test_get_request_with_wrong_secret(self):
        self._set_wrong_secret()
        result = self.exchanger._get_request(self.url).json()

        self.assertEqual(result['message'], 'Signature mismatch')
        self.assertEqual(result['label'], 'INVALID_SIGNATURE')

    def test_get_request_with_wrong_host(self):
        self._set_wrong_host()
        self._get_error_404(self.url)

    def test_get_request_with_wrong_prefix(self):
        self._set_wrong_prefix()
        self._get_error_404(self.url)

    def test_get_request_with_wrong_url(self):
        self._get_error_404(self.url_wrong)

