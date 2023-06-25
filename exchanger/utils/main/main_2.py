""""""

from copy import deepcopy

from cmc.handlers.cmc import Cmc
from exchanger.utils.main.exchanges import DataFromExchangers


class Main:
    """"""

    def __init__(self, user_id,):
        self.exchanges = DataFromExchangers(user_id)

    def get_data_from_exchangers(self):
        ## get info from exchangers for cryptocurrencies
        exchangers_data = self.exchanges.get_data_from_exchangers()

        return exchangers_data

    @staticmethod
    def get_aggregation_data(data_from_cmc, data_from_exchangers):
        """"""
        time_data = set()

        aggregation_data = deepcopy(data_from_exchangers)
        for exchanger in aggregation_data:
            for currency in list(exchanger.values())[0]:
                try:
                    currency.update(data_from_cmc[currency['coin']])
                    currency.update({'total': float(currency['bal']) * float(currency['price'])})
                    time_data.add(currency['coin'])
                except KeyError:
                    currency.update({'data': '---', 'id': '---', 'name': '---', 'price': 0, 'total': 0})

        w = []
        for symbol, value in data_from_cmc.items():
            if symbol in time_data:
                continue
            if symbol in ['IOTA']:
                continue
            else:
                w.append({'coin': symbol,
                          'bal': 0,
                          'data': value['data'],
                          'id': value['id'],
                          'name': value['name'],
                          'price': value['price'],
                          'total': 0
                          })

        aggregation_data.append({'others': w})

        return aggregation_data

    def chack_name(self, symbol):
        """HTTP method POST."""
        match symbol:
            case 'CFI':
                return 'CFi'
            case 'IOTA':
                return 'MIOTA'
            case _:
                return symbol

def main(user_id):
    """"""
    main = Main(user_id)

    data_from_exchangers = main.get_data_from_exchangers()
    # print(data_from_exchangers)

    symbol_list = []
    for data_from_exchanger in data_from_exchangers:
        symbol_list += [main.chack_name(coin['coin']) for coin in list(data_from_exchanger.values())[0]]
    # print('9------', sorted(symbol_list))

    cmc = Cmc(symbol_list)
    data_from_cmc = cmc.get_data_from_cmc()
    # print('6------', data_from_cmc)

    aggregation_data = main.get_aggregation_data(data_from_cmc, data_from_exchangers)
    # [print(e) for e in aggregation_data]

    return aggregation_data

