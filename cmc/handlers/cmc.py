""""""
import os

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dateutil import parser


from dotenv import load_dotenv

load_dotenv()


class Cmc:
    """"""

    def __init__(self, symbols: list[str]):

        self.symbols = ','.join(symbols)
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'  # Latest quotes
        self.api_cmc = os.environ.get('API_COINMARCETCAP')

        self.parameters = {
            'symbol': self.symbols,
            'convert': 'USD'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_cmc,
        }

    def get_cryptocurrency(self: str) -> dict[dict]:
        """"""
        session = Session()
        session.headers.update(self.headers)

        try:
            response = session.get(self.url, params=self.parameters)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            message = f'openweathermap.org returned non-200 code. Actual code is: {response.status_code},' \
                      f' message is: {response.json()["status"]["error_message"]}'
            print('error ----- ', message)
            raise RuntimeError(message)

        session.close()
        return response.json()

    def parse_cryptocurrencies(self, currencies_data: dict[dict]) -> dict[dict[str, dict]]:
        """Parse weather data"""
        currencies = {}
        for symbol in self.symbols.split(','):
            result = self.parse_cryptocurrencies_data(currencies_data, symbol)
            if not result:
                continue
            else:
                if symbol == 'MIOTA':
                    symbol = 'IOTA'
                currencies[symbol.upper()] = result
        return dict(sorted(currencies.items()))

    def parse_cryptocurrencies_data(self, currencies_data: dict[dict], symbol: str) -> dict[str, str]:
        """Parse data"""
        try:
            date = currencies_data['status']['timestamp']
        except KeyError:
            return {}

        try:
            currencies_data['data'][symbol]
        except KeyError:
            data = self.fill_values_if_is_not_symbol(date, symbol)
            return data

        id = currencies_data['data'][symbol]['id']
        name = currencies_data['data'][symbol]['name']
        symbol = currencies_data['data'][symbol]['symbol']
        price = currencies_data['data'][symbol]['quote']['USD']['price']

        data = {
            'data': parser.isoparse(date).strftime("%d-%m-%Y %H:%M:%S"),
            'id': id,
            'name': name,
            'coin': symbol.upper(),
            'price': price,
        }
        return data

    @staticmethod
    def fill_values_if_is_not_symbol(date: str, symbol: str) -> dict[str, str]:
        """"""
        result = {
            'data': parser.isoparse(date).strftime("%d-%m-%Y %H:%M:%S"),
            'id': 'not in CMC',
            'name': '---',
            'coin': symbol.upper(),
            'price': 0,
        }
        return result

    @staticmethod
    def normalize_data(data: list[str]) -> list[str]:
        return [value.upper() for value in data]

    def get_data(self):
        json_data = self.get_cryptocurrency()
        return self.parse_cryptocurrencies(json_data)

    def get_data_from_cmc(self):
        ## get info from coinmarketcap for cryptocurrencies
        cryptocurrencies_data = self.get_cryptocurrency()

        ## parse all data for using
        cryptocurrencies_data = self.parse_cryptocurrencies(cryptocurrencies_data)

        return cryptocurrencies_data