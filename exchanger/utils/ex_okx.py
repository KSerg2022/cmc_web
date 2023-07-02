import os

import okx.Account as Account
import okx.Funding as Funding
from okx.exceptions import OkxAPIException, OkxParamsException, OkxRequestException

from .ex_base import ExchangerBase, ERROR_MSG

from exchanger.models import Exchanger

from dotenv import load_dotenv

load_dotenv()


class ExOkx(ExchangerBase):

    def __init__(self, host=None, url=None, prefix=None,
                 api_key=None, api_secret=None, passphrase=None):
        self.host = host
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.params = {'api_key': self.api_key,
                       'api_secret_key': self.api_secret,
                       'passphrase': self.passphrase,
                       'domain': self.host,
                       'use_server_time': False,
                       'flag': '0',
                       'debug': False}

        self.account = Account.AccountAPI(**self.params)
        self.funding = Funding.FundingAPI(**self.params)
        self.exchanger = os.path.splitext(os.path.basename(__file__))[0][3:]

    def get_funding(self):
        """"""
        response = self._get_response(fn=self.funding.get_balances,
                                  error_label='funding',
                                  exchanger=self.exchanger,
                                  exception=(OkxAPIException,
                                             OkxParamsException,
                                             OkxRequestException))
        if response.get('msg', ''):
            return {'error': f'"{"funding".upper()}" - ERROR - "{ERROR_MSG}"'}
        return response

    def get_account_trading(self):
        """"""
        response = self._get_response(fn=self.account.get_account_balance,
                                      error_label='trading account',
                                      exchanger=self.exchanger,
                                      exception=(OkxAPIException,
                                                 OkxParamsException,
                                                 OkxRequestException))
        if response.get('msg', ''):
            return {'error': f'"{"trading account".upper()}" - ERROR - "{ERROR_MSG}"'}
        return response

    def get_account(self):
        """"""
        currencies_trading = self.get_account_trading()
        currencies_funding = self.get_funding()
        currencies = self._normalize_data(currencies_trading,
                                          currencies_funding)
        return currencies

    def _normalize_data(self, currencies_trading, currencies_funding):
        """"""
        if 'error' in currencies_trading and 'error' in currencies_funding:
            return {self.exchanger: [currencies_trading, currencies_funding]}

        currencies = []
        for symbol in currencies_trading['data'][0]['details'] + currencies_funding['data']:
            if y := [x for x in currencies if x['coin'] == symbol['ccy']]:
                currencies[currencies.index(y[0])] = {'coin': symbol['ccy'],
                                                      'bal': y[0]['bal'] + float(symbol['bal'])}
            else:
                try:
                    currencies.append({
                        'coin': symbol['ccy'],
                        'bal': float(symbol['eq'])
                    })
                except KeyError:
                    currencies.append({
                        'coin': symbol['ccy'].upper(),
                        'bal': float(symbol['bal'])
                    })
        return {self.exchanger: sorted(currencies, key=lambda x: x['coin'])}
