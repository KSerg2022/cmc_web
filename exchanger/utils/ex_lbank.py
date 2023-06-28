"""https://github.com/LBank-exchange/lbank-python-api/blob/master/LBank/rest.py"""
import os

from exchanger.utils.handlers.LBank import LBankAPI
from exchanger.utils.handlers.LBank import LBankError

from exchanger.utils.ex_base import ExchangerBase

from dotenv import load_dotenv

load_dotenv()


class ExLbank(ExchangerBase):
    """"""

    def __init__(self, host=None, url=None, prefix=None,
                 api_key=None, api_secret=None, passphrase=None):
        self.api_key = api_key
        self.private_key = api_secret
        self.api = LBankAPI(self.api_key, self.private_key)
        self.exchanger = os.path.splitext(os.path.basename(__file__))[0][3:]

    def get_account(self):
        """"""
        account = self._get_response(fn=self.api.user_assets,
                                     error_label='account',
                                     exchanger=self.exchanger,
                                     exception=(LBankError, ))
        currencies = self._normalize_data(account)
        return currencies

    def _normalize_data(self, currencies_account):
        """"""
        if 'error' in currencies_account:
            return {self.exchanger: [currencies_account]}

        currencies = []
        for symbol, value in currencies_account['info']['toBtc'].items():
            if float(value) != 0:
                currencies.append({
                    'coin': symbol.upper(),
                    'bal': value
                })
        return {self.exchanger: sorted(currencies, key=lambda x: x['coin'])}
