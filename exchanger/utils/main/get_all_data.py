""""""

from copy import deepcopy

from cmc.handlers.cmc import Cmc
from exchanger.utils.main.exchanges import DataFromExchangers


def get_data_from_exchangers(user_id):
    exchangers_data = DataFromExchangers(user_id).get_data_from_exchangers()
    return exchangers_data


def get_aggregation_data(data_from_cmc, data_from_exchangers):
    """"""
    time_data = set()

    aggregation_data = deepcopy(data_from_exchangers)
    for exchanger in aggregation_data:
        for currency in list(exchanger.values())[0]:
            if 'error' in currency:
                continue

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
            if symbol:
                w.append({'coin': symbol,
                          'bal': 0,
                          'data': value['data'],
                          'id': value['id'],
                          'name': value['name'],
                          'price': value['price'],
                          'total': 0
                          })
    if w:
        aggregation_data.append({'others': w})

    return aggregation_data


def check_name(symbol):
    """HTTP method POST."""
    match symbol:
        case 'CFI':
            return 'CFi'
        case 'IOTA':
            return 'MIOTA'
        case _:
            return symbol


def get_all_data(user_id):
    """"""

    data_from_exchangers = get_data_from_exchangers(user_id)

    symbol_list = []
    for data_from_exchanger in data_from_exchangers:
        if 'error' in list(data_from_exchanger.values())[0][0]:
            continue
        symbol_list += [check_name(coin['coin']) for coin in list(data_from_exchanger.values())[0]]

    cmc = Cmc(symbol_list)
    data_from_cmc = cmc.get_data_from_cmc()

    aggregation_data = get_aggregation_data(data_from_cmc, data_from_exchangers)
    return aggregation_data

