from exchanger.utils.main.get_all_data import get_aggregation_data
from cmc.handlers.cmc import Cmc
from exchanger.utils.ex_binance import ExBinance
from exchanger.utils.ex_bybit import ExBybit
from exchanger.utils.ex_gateio import ExGate
from exchanger.utils.ex_lbank import ExLbank
from exchanger.utils.ex_mexc import ExMexc
from exchanger.utils.ex_okx import ExOkx
from exchanger.utils.main.get_all_data import check_name


def select_exchanger(portfolio):
    """HTTP method POST."""
    name = portfolio.exchanger.name.upper()
    match name:
        case 'BINANCE':
            return ExBinance(api_key=portfolio.api_key,
                             api_secret=portfolio.api_secret
                             ).get_account()
        case 'BYBIT':
            return ExBybit(api_key=portfolio.api_key,
                           api_secret=portfolio.api_secret
                           ).get_account()
        case 'OKX':
            return ExOkx(host=portfolio.exchanger.host, api_key=portfolio.api_key,
                         api_secret=portfolio.api_secret, passphrase=portfolio.password
                         ).get_account()
        case 'LBANK':
            return ExLbank(api_key=portfolio.api_key,
                           api_secret=portfolio.api_secret
                           ).get_account()
        case 'MEXC':
            return ExMexc(host=portfolio.exchanger.host, api_key=portfolio.api_key,
                          api_secret=portfolio.api_secret, prefix=portfolio.exchanger.prefix,
                          url=portfolio.exchanger.url
                          ).get_account()
        case 'GATE':
            return ExGate(host=portfolio.exchanger.host, api_key=portfolio.api_key,
                          api_secret=portfolio.api_secret, prefix=portfolio.exchanger.prefix
                          ).get_account()
        case _:
            return 'Not allowed exchanger.'


def get_data(portfolio):
    """"""
    response_exchanger = select_exchanger(portfolio)

    if 'error' in list(response_exchanger.values())[0][0]:
        errors = list(response_exchanger.values())[0]
        return errors, 0

    symbol_list = [check_name(coin['coin']) for coin in list(response_exchanger.values())[0]]
    response_cmc = Cmc(symbol_list).get_data_from_cmc()
    data = get_aggregation_data(data_from_cmc=response_cmc,
                                data_from_exchangers=[response_exchanger])

    crypto_data = list(data[0].values())[0]
    total_sum = sum([coin['total'] for coin in crypto_data])
    return crypto_data, total_sum
