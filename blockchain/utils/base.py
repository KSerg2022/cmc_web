"""
Base class bo blockchains.
"""
import requests
from requests.exceptions import RequestException


from dotenv import load_dotenv
load_dotenv()

RATE_DECIMALS_9 = ['MCRT', ]


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
        for currency, contractaddress in self.currencies.items():
            self.params['contractaddress'] = contractaddress

            response = self._get_request(self.host, self.params, self.headers)
            if response['message'] == 'NOTOK':
                print(f"Error - {response['result']}, host={self.host}")
                return {self.blockchain: [response]}

            if currency in RATE_DECIMALS_9:
                currencies.append({self.COIN: currency, self.BAL: float(response['result']) / (10 ** 9)})
            else:
                currencies.append({self.COIN: currency, self.BAL: float(response['result']) / (10 ** 18)})
        return {self.blockchain: sorted(currencies, key=lambda x: x['coin'])}

    @staticmethod
    def _get_request(url: str, params: dict[str, str], headers=None) -> dict | None:
        """"""
        try:
            response = requests.request(method='GET', url=url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                e = f"Ошибка получения данных. Код ответа: {response.status_code}"
                print(e)
                return {'message': 'NOTOK', "result": e}
        except RequestException as e:
            print(f"Ошибка подключения: {str(e)}")
            return {'message': 'NOTOK', "result": str(e)}

    def get_account_balance(self) -> dict | None:
        """"""
        params = {'module': 'account',
                  'action': 'balance',
                  'address': self.wallet,
                  'apikey': self.api_key,
                  }
        result = self._get_request(self.host, params)
        return result

    def get_address_BEP20_token_holding(self):
        """API PRO need"""
        params = {'module': 'account',
                  'action': 'addresstokenbalance',
                  'address': self.wallet,
                  'page': 1,
                  'offset': 100,
                  'apikey': self.api_key,
                  }
        result = self._get_request(self.host, params)
        return result
