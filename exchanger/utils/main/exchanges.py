""""""
from django.shortcuts import get_object_or_404

from exchanger.utils.ex_lbank import ExLbank
from exchanger.utils.ex_mexc import ExMexc
from exchanger.utils.ex_binance import ExBinance

from exchanger.utils.ex_gateio import ExGate
from exchanger.utils.ex_bybit import ExBybit
from exchanger.utils.ex_okx import ExOkx

from blockchain.utils.bsc import Bsc
from blockchain.utils.ether import Ether
from blockchain.utils.fantom import Fantom
from blockchain.utils.polygon import Polygon
from blockchain.utils.solana import Solana

from django.contrib.auth.models import User


class DataFromExchangers:
    """"""

    def __init__(self, user_id):
        user_exchanger_portfolios = get_object_or_404(User,
                                                      id=user_id).exchanger_created.all()
        data_for_queries_exchanger = self.get_data_for_queries(user_exchanger_portfolios)

        user_blockchain_portfolios = get_object_or_404(User,
                                                       id=user_id).blockchain_created.all()
        data_for_queries_blockchain = self.get_data_for_queries_blockchain(user_blockchain_portfolios)

        self.currencies = []
        self.exchangers = [
            ExLbank(*data_for_queries_exchanger['Lbank']).get_account,
            ExMexc(*data_for_queries_exchanger['MEXC']).get_account,
            ExGate(*data_for_queries_exchanger['Gate']).get_account,
            ExBybit(*data_for_queries_exchanger['ByBit']).get_account,
            ExOkx(*data_for_queries_exchanger['OKX']).get_account,
            ExBinance(*data_for_queries_exchanger['Binance']).get_account,

            Bsc(*data_for_queries_blockchain['BSC']).get_account,
            Ether(*data_for_queries_blockchain['Ethereum']).get_account,
            Polygon(*data_for_queries_blockchain['Polygon']).get_account,
            Fantom(*data_for_queries_blockchain['Fantom']).get_account,
            Solana(*data_for_queries_blockchain['Solana']).get_account,
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

    def get_data_for_queries_blockchain(self, user_portfolios):
        data = {}
        for q in user_portfolios:
            data[q.blockchain.name] = (q.api_key,
                                       q.wallet,
                                       q.currencies)
        return data
