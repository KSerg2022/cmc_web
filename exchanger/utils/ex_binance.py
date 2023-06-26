"""
https://dev.binance.vision/t/ip-whitelist-does-not-have-effect/2767
https://algotrading101.com/learn/binance-python-api-guide/
"""
import os

from binance.client import Client
from binance.exceptions import BinanceAPIException

from exchanger.utils.ex_base import ExchangerBase

from dotenv import load_dotenv

load_dotenv()


class ExBinance(ExchangerBase):

    def __init__(self, host=None, url=None, prefix=None,
                 api_key=None, api_secret=None, passphrase=None):
        self.api_key = api_key
        self.api_secret = api_secret

        self.coin_m = Client(api_key=self.api_key, api_secret=self.api_secret)
        self.exchanger = os.path.splitext(os.path.basename(__file__))[0][3:]

    def get_futures_coin_account(self):
        futures_coin_account = self._get_response(self.coin_m.futures_coin_account,
                                                  self.exchanger,
                                                  (BinanceAPIException, ),
                                                  )
        if not futures_coin_account:
            return futures_coin_account
        return [x for x in futures_coin_account['assets'] if float(x['walletBalance']) != 0]

    def get_spot_account(self) -> list[dict]:
        spot_account = self._get_response(self.coin_m.get_account,
                                          self.exchanger,
                                          (BinanceAPIException,)
                                          )
        if not spot_account:
            return spot_account
        return [x for x in spot_account['balances'] if float(x['free']) != 0 or float(x['locked']) != 0]

    def get_account(self):
        spot_account = self.get_spot_account()
        futures_coin_account = self.get_futures_coin_account()
        currencies = self._normalize_data(spot_account,
                                          futures_coin_account)

        return currencies

    def _normalize_data(self, spot_account, futures_coin_account):
        """"""
        if not spot_account and not futures_coin_account:
            return {self.exchanger: {}}

        currencies = []
        for symbol in spot_account + futures_coin_account:
            if y := [x for x in currencies if x['coin'] == symbol['asset']]:
                try:
                    q = symbol['free'] + symbol['locked']
                except KeyError:
                    q = symbol['marginBalance']
                currencies[currencies.index(y[0])] = {'coin': symbol['asset'],
                                                      'bal': y[0]['bal'] + float(q)}
            else:
                try:
                    currencies.append({
                        'coin': symbol['asset'],
                        'bal': float(symbol['free']) + float(symbol['locked'])
                    })
                except KeyError:
                    currencies.append({
                        'coin': symbol['asset'],
                        'bal': float(symbol['marginBalance'])
                    })
        return {self.exchanger: sorted(currencies, key=lambda x: x['coin'])}
