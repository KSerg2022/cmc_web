"""
Base class bo blockchains.
"""
import requests
from requests.exceptions import RequestException, HTTPError

from dotenv import load_dotenv
load_dotenv()

RATE_DECIMALS_9 = ['MCRT', ]


ERROR_MSG = 'Check your "api key", "wallet address".'
ERROR_MSG_NOT_EMPTY = 'List of currencies cannot be empty!'


class Base:
    """"""
    COIN = 'coin'
    BAL = 'bal'

    def __init__(self):
        self.host = ''
        self.api_key = ''
        self.wallet = ''
        self.currencies = {}
        self.params = {}
        self.headers = {}
        self.blockchain = ''

    def get_account(self) -> dict[str, dict]:
        """"""
        currencies = []
        if not self.currencies:
            return {self.blockchain: [{'error': f'"{self.blockchain.upper()}" - ERROR - "{ERROR_MSG_NOT_EMPTY}"'}]}
        for currency, contractaddress in self.currencies.items():
            self.params['contractaddress'] = contractaddress

            try:
                response = self._get_request(self.host, self.params, self.headers)
            except (ValueError, AttributeError, RequestException, HTTPError) as e:
                # return {self.blockchain: [{'error': f'"{self.blockchain.upper()}" - ERROR - "{ERROR_MSG}"'}]}
                return {self.blockchain: [{'error': e.args[0]}]}

            if currency in RATE_DECIMALS_9:
                currencies.append({self.COIN: currency, self.BAL: float(response['result']) / (10 ** 9)})
            else:
                currencies.append({self.COIN: currency, self.BAL: float(response['result']) / (10 ** 18)})
        return {self.blockchain: sorted(currencies, key=lambda x: x['coin'])}

    def _get_request(self, url: str, params: dict[str, str], headers=None) -> dict | None:
        """"""
        try:
            response = requests.request(method='GET',
                                        url=url,
                                        params=params,
                                        headers=headers)
            if response.status_code == 404:
                raise HTTPError(response)
            response = response.json()
            try:
                if (response.get('message', '') == 'NOTOK') or ('error' in response):
                    raise ValueError({'error': f"{self.blockchain.upper()} - {response}"})
            except AttributeError as e:
                raise AttributeError({'error': f"{self.blockchain.upper()} - {e}"})
        except RequestException as e:
            raise RequestException({'error': f"{self.blockchain.upper()} - {e}"})
        return response



    # def get_account_balance(self) -> dict | None:
    #     """"""
    #     params = {'module': 'account',
    #               'action': 'balance',
    #               'address': self.wallet,
    #               'apikey': self.api_key,
    #               }
    #     result = self._get_request(self.host, params)
    #     return result

    # def get_address_BEP20_token_holding(self):
    #     """API PRO need"""
    #     params = {'module': 'account',
    #               'action': 'addresstokenbalance',
    #               'address': self.wallet,
    #               'page': 1,
    #               'offset': 100,
    #               'apikey': self.api_key,
    #               }
    #     result = self._get_request(self.host, params)
    #     return result
