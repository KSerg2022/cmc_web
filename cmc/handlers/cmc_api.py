""""""
import os

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, JSONDecodeError

from cmc.handlers.json_file import JsonFile

from dotenv import load_dotenv

load_dotenv()


class Cmc:
    """"""

    def __init__(self):
        self.json = JsonFile()
        # self.filename = 'cmc_currencies'
        self.filename = 'cryptocurrency'
        self.api_cmc = os.environ.get('API_COINMARCETCAP')

        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'  # Metadata
        self.parameters = {
            'id': '9',
            'skip_invalid': True
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_cmc,
        }

    def get_cryptocurrency(self):
        response = self.get_response()
        return self.parse_cryptocurrencies_info(response.json())


    def get_response(self: str):
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
        return response


    @staticmethod
    def parse_cryptocurrencies_info(response_data: dict[dict]) -> list[dict[str, str]]:
        """Parse weather data"""
        currencies = []
        for id, data in response_data['data'].items():
            if (description := data['description']) is None:
                description = '-'
            try:
                website = data['urls']['website'][0]
            except:
                website = ''
            data = {
                'model': 'cmc.cryptocurrency',
                'pk': id,
                'fields': {
                    'symbol': data['symbol'],
                    'name': data['name'],
                    'slug': data['slug'],
                    'logo': data['logo'],
                    'description': description,
                    'website': website,
                    'contract': '',
                }
            }
            currencies.append(data)
        return currencies


if __name__ == '__main__':
    result = Cmc()
    r = result.get_cryptocurrency()
    print(r)
