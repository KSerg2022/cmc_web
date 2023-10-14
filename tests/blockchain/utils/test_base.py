""""""
import sys

from pathlib import Path
from requests import RequestException

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

    def test_get_request(self):
        b_chain = self.base_chain
        params = self._get_params(wallet=b_chain.wallet,
                                  apikey=b_chain.api_key)
        result = b_chain._get_request(b_chain.host, params)

        self.assertTrue(isinstance(result, dict))
        self.assertEqual(result['message'], 'OK')
        self.assertTrue(isinstance(int(result['result']), int))

    def test_get_request_with_wrong_contract_address(self):
        params = self._get_params(contract_address='0',
                                  wallet=self.base_chain.wallet,
                                  apikey=self.base_chain.api_key)
        with self.assertRaises(ValueError) as e:
            self.base_chain._get_request(self.base_chain.host, params)

        self.assertIn(self.name, e.exception.args[0]['error'])

        match self.name:
            case 'BSC':
                self.assertIn("BSC - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid contractAddress format'}",
                              e.exception.args[0]['error'])
            case 'ETHER':
                self.assertIn("ETHER - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid contractAddress format'}",
                              e.exception.args[0]['error'])
            case 'POLYGON':
                self.assertIn(
                    "POLYGON - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid contractAddress format'}",
                    e.exception.args[0]['error'])
            case 'FANTOM':
                self.assertIn(
                    "FANTOM - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid contractAddress format'}",
                    e.exception.args[0]['error'])
            case 'SOLANA':
                self.assertIn({'error': 'SOLANA - <Response [404]>'}, e.exception.args[0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')

    def test_get_request_with_wrong_api(self):
        params = self._get_params(wallet=self.base_chain.wallet,
                                  apikey='wrong')
        with self.assertRaises(ValueError) as e:
            self.base_chain._get_request(self.base_chain.host, params)

        self.assertIn(self.name, e.exception.args[0]['error'])
        match self.name:
            case 'BSC':
                self.assertIn("BSC - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid API Key'}",
                              e.exception.args[0]['error'])
            case 'ETHER':
                self.assertIn("ETHER - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid API Key'}",
                              e.exception.args[0]['error'])
            case 'POLYGON':
                self.assertIn("POLYGON - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid API Key'}",
                              e.exception.args[0]['error'])
            case 'FANTOM':
                self.assertIn("FANTOM - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid API Key'}",
                              e.exception.args[0]['error'])
            case 'SOLANA':
                self.assertIn({'error': 'SOLANA - <Response [404]>'}, e.exception.args[0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')

    def test_get_request_with_empty_api(self):
        params = self._get_params(wallet=self.base_chain.wallet,
                                  apikey='')
        result = self.base_chain._get_request(self.base_chain.host, params)
        match self.name:
            case 'BSC':
                self.assertIn('OK-Missing/Invalid API Key, rate limit of 1/5sec applied', result['message'])
            case 'ETHER':
                self.assertIn('OK-Missing/Invalid API Key, rate limit of 1/5sec applied', result['message'])
            case 'POLYGON':
                self.assertIn('OK-Missing/Invalid API Key, rate limit of 1/5sec applied', result['message'])
            case 'FANTOM':
                self.assertIn('OK-Missing/Invalid API Key, rate limit of 1/5sec applied', result['message'])
            case 'SOLANA':
                self.assertIn({'error': 'SOLANA - <Response [404]>'}, result['message'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')

    def test_get_request_with_wrong_wallet(self):
        params = self._get_params(wallet='wrong',
                                  apikey=self.base_chain.api_key)
        with self.assertRaises(ValueError) as e:
            self.base_chain._get_request(self.base_chain.host, params)

        self.assertIn(self.name, e.exception.args[0]['error'])
        match self.name:
            case 'BSC':
                self.assertIn("{'status': '0', 'message': 'NOTOK', 'result': 'Error! Invalid address format'}",
                              e.exception.args[0]['error'])
            case 'ETHER':
                self.assertIn("ETHER - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Invalid address format'}",
                              e.exception.args[0]['error'])
            case 'POLYGON':
                self.assertIn(
                    "POLYGON - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Invalid address format'}",
                    e.exception.args[0]['error'])
            case 'FANTOM':
                self.assertIn("FANTOM - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Invalid address format'}",
                              e.exception.args[0]['error'])
            case 'SOLANA':
                self.assertIn({'error': 'SOLANA - <Response [404]>'}, e.exception.args[0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')

    def test_get_request_with_wrong_host(self):
        params = self._get_params(wallet=self.base_chain.wallet,
                                  apikey=self.base_chain.api_key)
        with self.assertRaises(RequestException) as e:
            self.base_chain._get_request('https://api.bscscan.com/wrong', params)

        self.assertIn(self.name, e.exception.args[0]['error'])

        match self.name:
            case 'BSC':
                self.assertIn('BSC - <Response [404]>', e.exception.args[0]['error'])
            case 'ETHER':
                self.assertIn('ETHER - <Response [404]>', e.exception.args[0]['error'])
            case 'POLYGON':
                self.assertIn('POLYGON - <Response [404]>', e.exception.args[0]['error'])
            case 'FANTOM':
                self.assertIn('FANTOM - <Response [404]>', e.exception.args[0]['error'])
            case 'SOLANA':
                self.assertIn('SOLANA - <Response [404]>', e.exception.args[0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')

    def test_get_request_with_wrong_module(self):
        params = self._get_params(module='wron',
                                  wallet=self.base_chain.wallet,
                                  apikey=self.base_chain.api_key)
        with self.assertRaises(ValueError) as e:
            self.base_chain._get_request(self.base_chain.host, params)

        self.assertIn(self.name, e.exception.args[0]['error'])

        match self.name:
            case 'BSC':
                self.assertIn(
                    "BSC - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Missing Or invalid Module name'}",
                    e.exception.args[0]['error'])
            case 'ETHER':
                self.assertIn(
                    "ETHER - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Missing Or invalid Module name'}",
                    e.exception.args[0]['error'])
            case 'POLYGON':
                self.assertIn(
                    "POLYGON - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Missing Or invalid Module name'}",
                    e.exception.args[0]['error'])
            case 'FANTOM':
                self.assertIn(
                    "FANTOM - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Missing Or invalid Module name'}",
                    e.exception.args[0]['error'])
            case 'SOLANA':
                self.assertIn({'error': 'SOLANA - <Response [404]>'}, e.exception.args[0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')

    def test_get_request_with_wrong_action(self):
        params = self._get_params(action='wron',
                                  wallet=self.base_chain.wallet,
                                  apikey=self.base_chain.api_key)
        with self.assertRaises(ValueError) as e:
            self.base_chain._get_request(self.base_chain.host, params)

        self.assertIn(self.name, e.exception.args[0]['error'])

        match self.name:
            case 'BSC':
                self.assertIn(
                    "BSC - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Missing Or invalid Action name'}",
                    e.exception.args[0]['error'])
            case 'ETHER':
                self.assertIn(
                    "ETHER - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Missing Or invalid Action name'}",
                    e.exception.args[0]['error'])
            case 'POLYGON':
                self.assertIn(
                    "POLYGON - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Missing Or invalid Action name'}",
                    e.exception.args[0]['error'])
            case 'FANTOM':
                self.assertIn(
                    "FANTOM - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Missing Or invalid Action name'}",
                    e.exception.args[0]['error'])
            case 'SOLANA':
                self.assertIn({'error': 'SOLANA - <Response [404]>'}, e.exception.args[0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')


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
        match self.name:
            case 'BSC':
                self.assertEqual({'error': "BSC - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid API Key'}"},
                                 list(result.values())[0][0]['error'])
            case 'ETHER':
                self.assertEqual({'error': "ETHER - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid API Key'}"},
                                 list(result.values())[0][0]['error'])
            case 'POLYGON':
                self.assertEqual(
                    {'error': "POLYGON - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid API Key'}"},
                    list(result.values())[0][0]['error'])
            case 'FANTOM':
                self.assertEqual({'error': "FANTOM - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid API Key'}"},
                                 list(result.values())[0][0]['error'])
            case 'SOLANA':
                self.assertEqual({'error': 'SOLANA - <Response [404]>'}, list(result.values())[0][0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')

    def test_get_account_with_wrong_wallet(self):
        self.base_chain.params = self._get_params(wallet='wrong',
                                                  apikey=self.base_chain.api_key)
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        match self.name:
            case 'BSC':
                self.assertEqual(
                    {'error': "BSC - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Invalid address format'}"},
                    list(result.values())[0][0]['error'])
            case 'ETHER':
                self.assertEqual(
                    {'error': "ETHER - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Invalid address format'}"},
                    list(result.values())[0][0]['error'])
            case 'POLYGON':
                self.assertEqual({
                    'error': "POLYGON - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Invalid address format'}"},
                    list(result.values())[0][0]['error'])
            case 'FANTOM':
                self.assertEqual({
                    'error': "FANTOM - {'status': '0', 'message': 'NOTOK', 'result': 'Error! Invalid address format'}"},
                    list(result.values())[0][0]['error'])
            case 'SOLANA':
                self.assertEqual({'error': 'SOLANA - <Response [404]>'}, list(result.values())[0][0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')

    def test_get_account_with_wrong_host(self):
        self.base_chain.host = 'https://api.bscscan.com/wrong'
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        match self.name:
            case 'BSC':
                self.assertEqual({'error': 'BSC - <Response [404]>'}, list(result.values())[0][0]['error'])
            case 'ETHER':
                self.assertEqual({'error': 'ETHER - <Response [404]>'}, list(result.values())[0][0]['error'])
            case 'POLYGON':
                self.assertEqual({'error': 'POLYGON - <Response [404]>'}, list(result.values())[0][0]['error'])
            case 'FANTOM':
                self.assertEqual({'error': 'FANTOM - <Response [404]>'}, list(result.values())[0][0]['error'])
            case 'SOLANA':
                self.assertEqual({'error': 'SOLANA - <Response [404]>'}, list(result.values())[0][0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')

    def test_get_account_with_wrong_host_(self):
        self.base_chain.host = 'ttps://api.bscscan.com/api'
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        match self.name:
            case 'BSC':
                self.assertEqual({'error': "BSC - No connection adapters were found for 'ttps://api.bscscan.com/api'"},
                                 list(result.values())[0][0]['error'])
            case 'ETHER':
                self.assertEqual(
                    {'error': "ETHER - No connection adapters were found for 'ttps://api.bscscan.com/api'"},
                    list(result.values())[0][0]['error'])
            case 'POLYGON':
                self.assertEqual(
                    {'error': "POLYGON - No connection adapters were found for 'ttps://api.bscscan.com/api'"},
                    list(result.values())[0][0]['error'])
            case 'FANTOM':
                self.assertEqual(
                    {'error': "FANTOM - No connection adapters were found for 'ttps://api.bscscan.com/api'"},
                    list(result.values())[0][0]['error'])
            case 'SOLANA':
                self.assertEqual({'error': 'SOLANA - <Response [404]>'}, list(result.values())[0][0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')

    def test_get_account_with_wrong_currencies(self):
        self.base_chain.currencies = {
            'BUSD': '0',
            'CAKE': '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82_', }
        result = self.base_chain.get_account()

        self.assertTrue(list(result.values())[0][0]['error'])
        match self.name:
            case 'BSC':
                self.assertEqual(
                    {'error': "BSC - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid contractAddress format'}"},
                    list(result.values())[0][0]['error'])
            case 'ETHER':
                self.assertEqual({
                    'error': "ETHER - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid contractAddress format'}"},
                    list(result.values())[0][0]['error'])
            case 'POLYGON':
                self.assertEqual({
                    'error': "POLYGON - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid contractAddress format'}"},
                    list(result.values())[0][0]['error'])
            case 'FANTOM':
                self.assertEqual({
                    'error': "FANTOM - {'status': '0', 'message': 'NOTOK', 'result': 'Invalid contractAddress format'}"},
                    list(result.values())[0][0]['error'])
            case 'SOLANA':
                self.assertEqual({'error': 'SOLANA - <Response [404]>'}, list(result.values())[0][0]['error'])
            case _:
                print(f'\n{self.name}: {__name__} - {sys._getframe().f_code.co_name}  - Not allowed exchanger.')
