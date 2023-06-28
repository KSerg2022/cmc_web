"""
https://www.gate.io/docs/developers/apiv4/#gate-api-v4-v4-46-0
"""
import os
import requests
import time
import hashlib
import hmac

from requests.exceptions import RequestException

from exchanger.utils.ex_base import ExchangerBase

from dotenv import load_dotenv

load_dotenv()


class ExGate(ExchangerBase):
    """"""

    def __init__(self, host=None, url=None, prefix=None,
                 api_key=None, api_secret=None, passphrase=None):
        self.host = host
        self.prefix = prefix
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.query_param = ''
        self.key = api_key  # api_key
        self.secret = api_secret  # api_secret
        self.exchanger = os.path.splitext(os.path.basename(__file__))[0][3:]

    def gen_sign(self, method, url, query_string=None, payload_string=None):
        """"""
        t = time.time()
        m = hashlib.sha512()
        m.update((payload_string or "").encode('utf-8'))
        hashed_payload = m.hexdigest()
        s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
        sign = hmac.new(self.secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
        return {'KEY': self.key, 'Timestamp': str(t), 'SIGN': sign}

    def get_total_balance(self):
        """in USDT"""
        url = '/wallet/total_balance'
        return self._get_response(fn=self._get_request,
                                  error_label='total balance',
                                  exchanger=self.exchanger,
                                  exception=(RequestException,),
                                  url=url)

    def get_account(self):
        """"""
        url = '/spot/accounts'
        currencies_account = self._get_response(fn=self._get_request,
                                                error_label='spot account',
                                                exchanger=self.exchanger,
                                                exception=(RequestException,),
                                                url=url)
        currencies = self._normalize_data(currencies_account)
        return currencies

    def _get_request(self, url):
        """"""
        sign_headers = self.gen_sign('GET', self.prefix + url, self.query_param)
        self.headers.update(sign_headers)
        return requests.request('GET', self.host + self.prefix + url, headers=self.headers)

    def _normalize_data(self, currencies_account: dict[list]):
        """"""
        if 'error' in currencies_account:
            return {self.exchanger: [currencies_account]}

        currencies = []
        for symbol in currencies_account.json():
            currencies.append({
                'coin': symbol['currency'].upper(),
                'bal': float(symbol['available']) + float(symbol['locked'])
            })
        return {self.exchanger: sorted(currencies, key=lambda x: x['coin'])}
