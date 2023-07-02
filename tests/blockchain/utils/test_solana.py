""""""
import unittest
import os
from django.test import TestCase

from pathlib import Path

from blockchain.utils.solana import Solana

from dotenv import load_dotenv

load_dotenv()

base_dir = Path(__file__).parent.parent


class TestSolana(TestCase):

    def setUp(self) -> None:
        self.name = 'SOLANA'
        self.host = 'https://public-api.solscan.io/account/tokens'
        self.api_key = os.environ.get('SOLANA_API_KEY')
        self.wallet = os.environ.get('WALLET_SOLANA')
        self.currencies = {"BGS": "At7RLMbA6ZUjj7riyvFq2j5NHQ19aJabCju2VxLDAqso",
                           "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"}

        self.base_chain = Solana(host=self.host,
                              api_key=self.api_key,
                              wallet=self.wallet,
                              currencies=self.currencies)

    def tearDown(self) -> None:
        del self.base_chain

    def _get_params(self, wallet=None):
        if wallet is None:
            wallet = self.base_chain.wallet
        return {'account': wallet}

    def _get_headers(self, api_key=None):
        if api_key is None:
            api_key = self.base_chain.api_key
        return {'account': api_key}


class TestSolanaGetRequest(TestSolana):

    def test__get_request(self):
        response = self.base_chain._get_request(self.base_chain.host,
                                             self.base_chain.params,
                                             self.base_chain.headers)

        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], dict)
        self.assertIsNotNone(response[0]['tokenAddress'])

    def test__get_request_with_wrong_api(self):
        self.base_chain.headers = self._get_headers(api_key='wrong')
        result = self.base_chain._get_request(self.base_chain.host,
                                           self.base_chain.params,
                                           self.base_chain.headers)

        self.assertTrue(result['error'])
        self.assertIn(self.name, result['error'])
        self.assertIn('Expecting value', result['error'])

    def test__get_request_with_wrong_wallet(self):
        self.base_chain.params = self._get_params(wallet='0')
        result = self.base_chain._get_request(self.base_chain.host,
                                           self.base_chain.params,
                                           self.base_chain.headers)

        self.assertTrue(result['error'])
        self.assertIn(self.name, result['error'])
        self.assertIn('Check your "api key", "wallet address"', result['error'])

    def test__get_request_with_wrong_host(self):
        result = self.base_chain._get_request('https://public-api.solscan.io/wrong',
                                             self.base_chain.params,
                                             self.base_chain.headers)

        self.assertTrue(result['error'])
        self.assertIn(self.name, result['error'])
        self.assertIn('Expecting value', result['error'])


class testSolanaGetAccount(TestSolana):

    def test_get_account(self):
        result = self.base_chain.get_account()

        self.assertIsInstance(result, dict)
        self.assertIsInstance(list(result.values())[0], list)
        self.assertIn(self.base_chain.COIN, list(result.values())[0][0])
        self.assertIn(self.base_chain.BAL, list(result.values())[0][0])

    def test_get_account_with_wrong_api(self):
        self.base_chain.headers = self._get_headers(api_key='wrong')
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        self.assertIn('Expecting value:', list(result.values())[0][0]['error'])

    def test_get_account_with_wrong_wallet(self):
        self.base_chain.params = self._get_params(wallet='0')
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        self.assertIn('Check your "api key", "wallet address"', list(result.values())[0][0]['error'])

    def test_get_account_with_wrong_host(self):
        self.base_chain.host = 'https://public-api.solscan.io/wrong'
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        self.assertIn('Expecting value:', list(result.values())[0][0]['error'])

    def test_get_account_with_wrong_currencies(self):
        self.base_chain.currencies = {'BUSD': 'wrong'}
        result = self.base_chain.get_account()

        self.assertIsInstance(result, dict)
        self.assertIsInstance(list(result.values())[0], list)
        self.assertIn(self.base_chain.COIN, list(result.values())[0][0])
        self.assertIn(self.base_chain.BAL, list(result.values())[0][0])
