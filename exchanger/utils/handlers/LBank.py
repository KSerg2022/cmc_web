import requests
import time
import json
from hashlib import md5
from base64 import b64encode

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

LBANK_ERROR_CODE = {

    '10000': 'Internal error',
    '10001': 'The necessary parameters can not be empty',
    '10002': 'Validation does not pass',
    '10003': 'Invalid parameter',
    '10004': 'User requests are too frequent',
    '10005': 'Secret key does not exist',
    '10006': 'User does not exist',
    '10007': 'Invalid sign',
    '10008': 'This transaction pair is not supported',
    '10009': 'The limit order should not be short of the price and the number of the orders',
    '10010': 'A single price or a single number must be more than 0',
    '10013': 'The minimum amount of sale that is less than the position of 0.001',
    '10014': 'Insufficient amount of money in account',
    '10015': 'Order type error',
    '10016': 'Insufficient account balance',
    '10017': 'Server exception',
    '10018': 'The number of order query entries should not be larger than 50 less than 1 bars',
    '10019': 'The number of withdrawal entries should not be greater than 3 less than 1',
    '10020': 'Minimum amount of sale less than 0.001',
    '10022': 'Access denied',
    '10025': 'Order filled',

}


class LBankError(RuntimeError):
    def __init__(self, code, msg):
        super().__init__(msg)
        self.code = code


def check_result(result):
    '''Raise LBank Error if it returned an error code'''
    if 'result' in result and result['result'] == 'false':
        code = result['error_code']
        msg = LBANK_ERROR_CODE.get(str(code), 'Unknown Error')
        raise LBankError(code, msg)
    else:
        return result


class LBankAPI:
    '''LBank API'''

    LBANK_API_URL = 'https://api.lbkex.com/'
    PAIR_QUOTATION_URL = LBANK_API_URL + 'v1/ticker.do'
    ALL_PAIR_DATA = LBANK_API_URL + 'v1/accuracy.do'
    AVAILABLE_PAIR_URL = LBANK_API_URL + 'v1/currencyPairs.do'
    MARKET_DEPTH_URL = LBANK_API_URL + 'v1/depth.do'
    HISTORICAL_TRANSACTION_URL = LBANK_API_URL + 'v1/trades.do'
    KLINE_DATA_URL = LBANK_API_URL + 'v1/kline.do'
    GET_USER_ASSETS_URL = LBANK_API_URL + 'v1/user_info.do'
    PLACE_AN_ORDER = LBANK_API_URL + 'v1/create_order.do'
    QUERY_ORDER = LBANK_API_URL + 'v1/orders_info.do'
    REVOCATION_OF_ORDER = LBANK_API_URL + 'v1/cancel_order.do'
    QUERY_ORDER_HISTORY = LBANK_API_URL + 'v1/orders_info_history.do'
    ACCESS_TO_OPEN_ORDER_FOR_USER = LBANK_API_URL + 'v1/orders_info_no_deal.do'

    def __init__(self, api_key=None, private_key=None):
        self._head = {'contentType': 'application/x-www-form-urlencoded'}
        self._api_key = api_key
        if private_key:
            if len(private_key) > 32:
                if private_key.split('\n')[0] == '-----BEGIN RSA PRIVATE KEY-----':
                    pass
                else:
                    private_key = '\n'.join([
                        '-----BEGIN RSA PRIVATE KEY-----',
                        private_key,
                        '-----END RSA PRIVATE KEY-----'
                    ])

                private_key = RSA.importKey(private_key)
                self._signer = PKCS1_v1_5.new(private_key)
            else:
                self._signer = None
                self._private_key = private_key
        else:
            self._signer = self._private_key = None

    def _generate_signature(self, parms):
        if self._signer:
            parms = ['%s=%s' % i for i in sorted(parms.items())]
            parms = '&'.join(parms).encode('utf-8')
            message = md5(parms).hexdigest().upper()

            digest = SHA256.new()
            digest.update(message.encode('utf-8'))
            signature = b64encode(self._signer.sign(digest))
        elif self._private_key:
            parms = ['%s=%s' % i for i in sorted(parms.items())]
            parms = '&'.join(parms) + '&secret_key=' + self._private_key
            signature = md5(parms.encode('utf-8')).hexdigest().upper()
        else:
            raise LBankError(10005, LBANK_ERROR_CODE['10005'])

        return signature

    def _requests_parms(self, api_key=None, symbol=None, size=None, merge=None,
                        time=None, type=None, price=None, amount=None, order_id=None, current_page=None,
                        page_length=None):
        requests_data = {}
        handle_data = {'api_key': api_key, 'symbol': symbol, 'size': size, 'merge': merge,
                       'time': time, 'type': type, 'price': price, 'amount': amount, 'order_id': order_id,
                       'current_page': current_page, 'page_length': page_length}
        for k, v in handle_data.items():
            if v:
                requests_data[k] = v
        return requests_data

    def _init_session(self, url, re_dict):
        session = requests.session()
        session.headers.update({'contentType': 'application/x-www-form-urlencoded'})
        if re_dict.get('api_key', None):
            re_dict['sign'] = self._generate_signature(re_dict)
            return session.post(url=url, data=re_dict)
        else:
            return session.get(url=url, params=re_dict)

    def _request(self, url, **parms):
        data = self._requests_parms(**parms)
        result = self._init_session(url, data).text
        return check_result(json.loads(result))

    def pair_quotation(self, symbol):
        '''Get the market'''
        url = self.PAIR_QUOTATION_URL
        return self._request(url, symbol=symbol)

    def available(self):
        '''Access to the LBank available Transaction pair to interface'''
        url = self.AVAILABLE_PAIR_URL
        return self._request(url)

    def market_depth(self, symbol, size, merge):
        '''Get the depth ofLBank,1 <= size <= 60, merge: 0 or 1'''
        url = self.MARKET_DEPTH_URL
        return self._request(url, symbol=symbol, size=size, merge=merge)

    def historical_transaction(self, symbol, size, start_time):
        '''Access to LBank historical transaction information, 1 <= size <= 600, start_time: %Y-%m-%d %H-%M'''
        tm = time.strptime(start_time, '%Y-%m-%d %H:%M')
        t = int(time.mktime(tm))
        url = self.HISTORICAL_TRANSACTION_URL
        return self._request(url, symbol=symbol, size=size, time=t)

    def kline_data(self, symbol, size, type, start_time):
        '''Get the K-line data,1 <= size <= 2880, start_time: %Y-%m-%d %H-%M
            tyoe:minute1：1minute
                minute5：5minute
                minute15：15minute
                minute30：30minute
                hour1：1hour
                hour4：4hour
                hour8：8hour
                hour12：12hour
                day1：1day
                week1：1week
        '''

        tm = time.strptime(start_time, '%Y-%m-%d %H:%M')
        t = int(time.mktime(tm))
        url = self.KLINE_DATA_URL
        return self._request(url, symbol=symbol, size=size, type=type, time=t)

    def essential_information(self):
        '''Get the basic information of all the money pairs'''
        url = self.ALL_PAIR_DATA
        return self._request(url)

    def user_assets(self):
        '''Access to user account asset information'''
        url = self.GET_USER_ASSETS_URL
        return self._request(url, api_key=self._api_key)

    def place_order(self, symbol, type, price, amount):
        '''Place an order,type: buy or sell ,price>=0 ,amount>=00.1'''
        url = self.PLACE_AN_ORDER
        return self._request(url, api_key=self._api_key, symbol=symbol, type=type, price=price, amount=amount)

    def query_order(self, symbol, order_id):
        '''Query order'''
        url = self.QUERY_ORDER
        return self._request(url, api_key=self._api_key, symbol=symbol, order_id=order_id)

    def cancel_the_order(self, symbol, order_id):
        '''Cancel the order'''
        url = self.REVOCATION_OF_ORDER
        return self._request(url, api_key=self._api_key, symbol=symbol, order_id=order_id)

    def query_h_order(self, symbol, current_page, page_length):
        '''Query order history,1<= page_length <= 200'''
        url = self.QUERY_ORDER_HISTORY
        return self._request(url, api_key=self._api_key, symbol=symbol, current_page=current_page,
                             page_length=page_length)

    def open_order(self, symbol, current_page, page_length):
        '''Access to open orders for users,1<= page_length <= 200'''
        url = self.ACCESS_TO_OPEN_ORDER_FOR_USER
        return self._request(url, api_key=self._api_key, symbol=symbol, current_page=current_page,
                             page_length=page_length)
