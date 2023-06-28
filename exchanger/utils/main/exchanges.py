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
        self.data_for_queries_exchanger = self.get_data_for_queries_exchanger(user_id)
        self.data_for_queries_blockchain = self.get_data_for_queries_blockchain(user_id)
        self.currencies = []

    def get_data_from_exchangers(self):
        """"""
        exchanger_list = list(self.data_for_queries_exchanger.keys())
        if 'Lbank' in exchanger_list:
            self.currencies.append(
                ExLbank(*self.data_for_queries_exchanger['Lbank']).get_account()
            )
        if 'MEXC' in exchanger_list:
            self.currencies.append(
                ExMexc(*self.data_for_queries_exchanger['MEXC']).get_account()
            )
        if 'ByBit' in exchanger_list:
            self.currencies.append(
                ExBybit(*self.data_for_queries_exchanger['ByBit']).get_account()
            )
        if 'Gate' in exchanger_list:
            self.currencies.append(
                ExGate(*self.data_for_queries_exchanger['Gate']).get_account()
            )
        if 'OKX' in exchanger_list:
            self.currencies.append(
                ExOkx(*self.data_for_queries_exchanger['OKX']).get_account()
            )
        if 'Binance' in exchanger_list:
            self.currencies.append(
                ExBinance(*self.data_for_queries_exchanger['Binance']).get_account()
            )

        blockchain_list = list(self.data_for_queries_blockchain.keys())
        if 'BSC' in blockchain_list:
            self.currencies.append(
                Bsc(*self.data_for_queries_blockchain['BSC']).get_account()
            )
        if 'Ethereum' in blockchain_list:
            self.currencies.append(
                Ether(*self.data_for_queries_blockchain['Ethereum']).get_account()
            )
        if 'Polygon' in blockchain_list:
            self.currencies.append(
                Polygon(*self.data_for_queries_blockchain['Polygon']).get_account()
            )
        if 'Fantom' in blockchain_list:
            self.currencies.append(
                Fantom(*self.data_for_queries_blockchain['Fantom']).get_account()
            )
        if 'Solana' in blockchain_list:
            self.currencies.append(
                Solana(*self.data_for_queries_blockchain['Solana']).get_account()
            )
        return self.currencies

    @staticmethod
    def get_data_for_queries_exchanger(user_id):
        user_exchanger_portfolios = get_object_or_404(User,
                                                      id=user_id).exchanger_created.all()
        data = {}
        for q in user_exchanger_portfolios:
            data[q.exchanger.name] = (q.exchanger.host,
                                      q.exchanger.url,
                                      q.exchanger.prefix,
                                      q.api_key,
                                      q.api_secret,
                                      q.password)
        return data

    @staticmethod
    def get_data_for_queries_blockchain(user_id):
        user_blockchain_portfolios = get_object_or_404(User,
                                                       id=user_id).blockchain_created.all()
        data = {}
        for q in user_blockchain_portfolios:
            data[q.blockchain.name] = (q.blockchain.host,
                                       q.api_key,
                                       q.wallet,
                                       q.currencies)
        return data
