
from dotenv import load_dotenv

load_dotenv()

ERROR_MSG = 'Check your "api key", "api secret", for "OKX" - "password". Check permissions for action (ip, ...).'


class ExchangerBase:

    @staticmethod
    def _get_response(fn, error_label=None, exchanger=None, exception=None,  accountType=None, url=None) -> dict | list:
        try:
            if accountType:
                response = fn(accountType=accountType)
            elif url:
                response = fn(url=url)
            else:
                response = fn()
        except (Exception, *exception) as e:
            # print(f'{exchanger.upper()} -- {e}')
            return {'error': f'"{error_label.upper()}" - ERROR - "{ERROR_MSG}"'}


        try:
            if response.status_code != 200:
                return {'error': f'"{error_label.upper()}" - ERROR - "{ERROR_MSG}"'}
        except AttributeError as e:
            pass
        return response
