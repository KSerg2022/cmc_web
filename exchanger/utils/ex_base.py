
from dotenv import load_dotenv

load_dotenv()


class ExchangerBase:

    @staticmethod
    def _get_response(fn, exchanger=None, exception=None,  accountType=None, url=None) -> dict | list:
        try:
            if accountType:
                response = fn(accountType=accountType)
            elif url:
                response = fn(url=url)
            else:
                response = fn()
        except (Exception, *exception) as e:
            print(f'{exchanger.upper()} -- {e}')
            return {}
        try:
            if response.status_code != 200:
                return {}
        except AttributeError:
            pass
        return response
