from blockchain.utils.bsc import Bsc
from blockchain.utils.ether import Ether
from blockchain.utils.fantom import Fantom
from blockchain.utils.polygon import Polygon
from blockchain.utils.solana import Solana
from exchanger.utils.main.get_all_data import get_aggregation_data
from cmc.handlers.cmc import Cmc

from exchanger.utils.main.get_all_data import check_name


def select_blockchain(portfolio):
    """HTTP method POST."""
    name = portfolio.blockchain.name.upper()
    match name:
        case 'BSC':
            return Bsc(host=portfolio.blockchain.host,
                       api_key=portfolio.blockchain.api_key,
                       wallet=portfolio.wallet,
                       currencies=portfolio.currencies).get_account()
        case 'ETHEREUM':
            return Ether(host=portfolio.blockchain.host,
                         api_key=portfolio.blockchain.api_key,
                         wallet=portfolio.wallet,
                         currencies=portfolio.currencies).get_account()
        case 'POLYGON':
            return Polygon(host=portfolio.blockchain.host,
                           api_key=portfolio.blockchain.api_key,
                           wallet=portfolio.wallet,
                           currencies=portfolio.currencies).get_account()
        case 'FANTOM':
            return Fantom(host=portfolio.blockchain.host,
                          api_key=portfolio.blockchain.api_key,
                          wallet=portfolio.wallet,
                          currencies=portfolio.currencies).get_account()
        case 'SOLANA':
            return Solana(host=portfolio.blockchain.host,
                          api_key=portfolio.blockchain.api_key,
                          wallet=portfolio.wallet,
                          currencies=portfolio.currencies).get_account()

        case _:
            return 'Not allowed exchanger.'


def get_data(portfolio):
    """"""
    response_blockchain = select_blockchain(portfolio)

    if 'error' in list(response_blockchain.values())[0][0]:
        errors = list(response_blockchain.values())[0]
        return errors, 0

    symbol_list = [check_name(coin['coin']) for coin in list(response_blockchain.values())[0]]
    response_cmc = Cmc(symbol_list).get_data_from_cmc()
    data = get_aggregation_data(data_from_cmc=response_cmc,
                                data_from_exchangers=[response_blockchain])
    crypto_data = list(data[0].values())[0]
    total_sum = sum([coin['total'] for coin in crypto_data])
    return crypto_data, total_sum
