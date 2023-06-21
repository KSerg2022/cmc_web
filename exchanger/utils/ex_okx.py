import os

import okx.Account as Account
import okx.Funding as Funding
from okx.exceptions import OkxAPIException, OkxParamsException, OkxRequestException

from .ex_base import ExchangerBase

from exchanger.models import Exchanger

from dotenv import load_dotenv

load_dotenv()


class ExOkx(ExchangerBase):
    host = "https://www.okx.com"

    def __init__(self, api_key, api_secret, passphrase):
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
        return self._get_response(self.funding.get_balances, self.exchanger, (OkxAPIException,
                                                                              OkxParamsException,
                                                                              OkxRequestException))

    def get_account_trading(self):
        """"""
        return self._get_response(self.account.get_account_balance, self.exchanger, (OkxAPIException,
                                                                                     OkxParamsException,
                                                                                     OkxRequestException))

    def get_account(self):
        """"""
        currencies_trading = self.get_account_trading()
        currencies_funding = self.get_funding()
        currencies = self._normalize_data(currencies_trading,
                                          currencies_funding)
        return currencies

    def _normalize_data(self, currencies_trading, currencies_funding):
        """"""
        if not currencies_trading and not currencies_funding:
            return {self.exchanger: {}}

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


if __name__ == '__main__':
    currencies = ExOkx()
    data = currencies.get_account()
    print(data)
