"""
https://mxcdevelop.github.io/apidocs/spot_v3_en/#introduction
"""
import os
import requests
import urllib.parse

from datetime import datetime
from requests.exceptions import RequestException
from MexcClient.Utils.Signature import generate_signature

from exchanger.utils.ex_base import ExchangerBase

from dotenv import load_dotenv

load_dotenv()


class ExMexc(ExchangerBase):
    """"""
    host = "https://api.mexc.com"
    prefix = "/api/v3/"
    url = 'account'

    def __init__(self, api_key, api_secret, passphrase):
        self.apiKey = api_key
        self.apiSecret = api_secret
        self.headers = {"X-MEXC-APIKEY": self.apiKey, "Content-Type": "application/json"}
        self.exchanger = os.path.splitext(os.path.basename(__file__))[0][3:]

    def gen_sign(self):
        """"""
        params = {"timestamp": int(datetime.now().timestamp()) * 1000}
        str_params = urllib.parse.urlencode(params)
        signature = generate_signature(self.apiSecret.encode(), str_params.encode())
        params["signature"] = signature
        return params

    def get_account(self):
        """"""
        currencies_account = self._get_response(self._get_request,
                                                self.exchanger,
                                                (RequestException, )
                                                )
        currencies = self._normalize_data(currencies_account.json())
        return currencies

    def _get_request(self):
        """"""
        sign_params = self.gen_sign()
        return requests.request('GET', self.host + self.prefix + self.url,
                                headers=self.headers,
                                params=sign_params)

    def _normalize_data(self, currencies_account):
        """"""
        if not currencies_account:
            return {self.exchanger: currencies_account}

        currencies = []
        for symbol in currencies_account['balances']:
            currencies.append({
                'coin': symbol['asset'].upper(),
                'bal': float(symbol['free']) + float(symbol['locked'])
            })
        return {self.exchanger: sorted(currencies, key=lambda x: x['coin'])}


if __name__ == '__main__':
    currencies = ExMexc()
    result = currencies.get_account()
    print(result)

