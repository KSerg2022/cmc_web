""""""

# from exchanger.utils.ex_lbank import ExLbank
# from exchanger.utils.ex_mexc import ExMexc
from django.shortcuts import get_object_or_404

from exchanger.utils.ex_gateio import ExGate
from exchanger.utils.ex_bybit import ExBybit
from exchanger.utils.ex_okx import ExOkx

# from exchanger.utils.ex_binance import ExBinance

# from exchanger.utils.bsc import Bsc
# from exchanger.utils.ether import Ether
# from exchanger.utils.fantom import Fantom
# from exchanger.utils.polygon import Polygon
# from exchanger.utils.solana import Solana

from django.contrib.auth.models import User


class DataFromExchangers:
    """"""

    def __init__(self, user_id):
        user_portfolios = get_object_or_404(User,
                                            id=user_id).exchanger_created.all()

        data_for_queries = self.get_data_for_queries(user_portfolios)
        self.currencies = []
        self.exchangers = [
            # ExLbank().get_account,
            # ExMexc().get_account,
            ExGate(*data_for_queries['Gate']).get_account,
            ExBybit(*data_for_queries['ByBit']).get_account,
            ExOkx(*data_for_queries['OKX']).get_account,
            # ExBinance().get_account,

            # Bsc().get_account,
            # Ether().get_account,
            # Polygon().get_account,
            # Fantom().get_account,
            # Solana().get_account,
        ]

    def get_data_from_exchangers(self):
        """"""
        for exchanger in self.exchangers:
            self.currencies.append(exchanger())
        return self.currencies

    def get_data_for_queries(self, user_portfolios):
        data = {}
        for q in user_portfolios:
            data[q.exchanger.name] = (q.api_key,
                                      q.api_secret,
                                      q.password)
        return data
