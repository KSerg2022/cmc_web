""""""
import unittest


from pathlib import Path

from blockchain.utils.base import Base

from dotenv import load_dotenv

load_dotenv()

base_dir = Path(__file__).parent.parent


class TestBase:

    def setUp(self) -> None:
        self.name = None
        self.base_chain = Base()
        self.contract_address = ''

    def tearDown(self) -> None:
        del self.base_chain

    def _get_params(self,
                    module='account',
                    action='tokenbalance',
                    contract_address=None,
                    wallet=None,
                    apikey=None):

        if contract_address is None:
            contract_address = self.contract_address
        return {'module': module,
                'action': action,
                'contractaddress': contract_address,
                'address': wallet,
                'tag': 'latest',
                'apikey': apikey,
                }

    def assertIsInstance(self, param, list):
        pass

    def assertIn(self, exchanger, result):
        pass

    def assertEqual(self, param, param1):
        pass

    def assertTrue(self, param):
        pass


class TestBaseGetRequest(TestBase):

    def test__get_request(self):
        b_chain = self.base_chain
        params = self._get_params(wallet=b_chain.wallet,
                                  apikey=b_chain.api_key)
        result = b_chain._get_request(b_chain.host, params)

        self.assertTrue(isinstance(result, dict))
        self.assertEqual(result['message'], 'OK')
        self.assertTrue(isinstance(int(result['result']), int))

    def test__get_request_with_wrong_contract_address(self):
        params = self._get_params(contract_address='0',
                                  wallet=self.base_chain.wallet,
                                  apikey=self.base_chain.api_key)
        result = self.base_chain._get_request(self.base_chain.host, params)

        self.assertTrue(result['error'])
        self.assertIn(self.name, result['error'])
        self.assertIn('Check your "api key", "wallet address"', result['error'])

    def test__get_request_with_wrong_api(self):
        params = self._get_params(wallet=self.base_chain.wallet,
                                  apikey='wrong')
        result = self.base_chain._get_request(self.base_chain.host, params)

        self.assertTrue(result['error'])
        self.assertIn(self.name, result['error'])
        self.assertIn('Check your "api key", "wallet address"', result['error'])

    def test__get_request_with_empty_api(self):
        params = self._get_params(wallet=self.base_chain.wallet,
                                  apikey='')
        result = self.base_chain._get_request(self.base_chain.host, params)

        self.assertIn('OK-Missing/Invalid API Key', result['message'])

    def test__get_request_with_wrong_wallet(self):
        params = self._get_params(wallet='wrong',
                                  apikey=self.base_chain.api_key)
        result = self.base_chain._get_request(self.base_chain.host, params)

        self.assertIn(self.name, result['error'])
        self.assertIn('Check your "api key", "wallet address"', result['error'])

    def test__get_request_with_wrong_host(self):
        params = self._get_params(wallet=self.base_chain.wallet,
                                  apikey=self.base_chain.api_key)
        result = self.base_chain._get_request('https://api.bscscan.com/wrong', params)

        self.assertIn(self.name, result['error'])
        self.assertIn('"Expecting value:', result['error'])

    def test__get_request_with_wrong_module(self):
        params = self._get_params(module='wron',
                                  wallet=self.base_chain.wallet,
                                  apikey=self.base_chain.api_key)
        result = self.base_chain._get_request(self.base_chain.host, params)

        self.assertIn(self.name, result['error'])
        self.assertIn('Check your "api key", "wallet address"', result['error'])

    def test__get_request_with_wrong_action(self):
        params = self._get_params(action='wron',
                                  wallet=self.base_chain.wallet,
                                  apikey=self.base_chain.api_key)
        result = self.base_chain._get_request(self.base_chain.host, params)

        self.assertIn(self.name, result['error'])
        self.assertIn('Check your "api key", "wallet address"', result['error'])


class TestBaseGetAccount(TestBase):

    def test_get_account(self):
        result = self.base_chain.get_account()

        self.assertTrue(isinstance(result, dict))
        self.assertTrue(isinstance(list(result.values())[0], list))
        self.assertIn(self.base_chain.COIN, list(result.values())[0][0])
        self.assertIn(self.base_chain.BAL, list(result.values())[0][0])

    def test_get_account_with_wrong_api(self):
        self.base_chain.params = self._get_params(wallet=self.base_chain.wallet,
                                                  apikey='wrong')
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        self.assertIn('Check your "api key", "wallet address"', list(result.values())[0][0]['error'])

    def test_get_account_with_wrong_wallet(self):
        self.base_chain.params = self._get_params(wallet='wrong',
                                                  apikey=self.base_chain.api_key)
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        self.assertIn('Check your "api key", "wallet address"', list(result.values())[0][0]['error'])

    def test_get_account_with_wrong_host(self):
        self.base_chain.host = 'https://api.bscscan.com/wrong'
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        self.assertIn('Expecting value', list(result.values())[0][0]['error'])

    def test_get_account_with_wrong_host_(self):
        self.base_chain.host = 'ttps://api.bscscan.com/api'
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        self.assertIn('No connection adapters', list(result.values())[0][0]['error'])

    def test_get_account_with_wrong_currencies(self):
        self.base_chain.currencies = {
            'BUSD': '0',
            'CAKE': '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82_', }
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        self.assertIn('Check your "api key", "wallet address"', list(result.values())[0][0]['error'])

