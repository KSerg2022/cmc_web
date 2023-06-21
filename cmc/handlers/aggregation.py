""""""

from copy import deepcopy


def get_aggregation_data(data_from_cmc=None, data_from_exchangers=None):
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

