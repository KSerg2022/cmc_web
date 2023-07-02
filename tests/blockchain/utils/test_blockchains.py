""""""
import os
import unittest
from django.test import TestCase

from pathlib import Path

from blockchain.utils.bsc import Bsc
from blockchain.utils.polygon import Polygon
from blockchain.utils.ether import Ether
from blockchain.utils.fantom import Fantom
from tests.blockchain.utils.test_base import (TestBaseGetRequest,
                                              TestBaseGetAccount)


from dotenv import load_dotenv

load_dotenv()

base_dir = Path(__file__).parent.parent


class TestBsc(TestCase, TestBaseGetRequest, TestBaseGetAccount):

    def setUp(self) -> None:
        self.name = 'BSC'
        self.host = 'https://api.bscscan.com/api'
        self.api_key = os.environ.get('BSCSCAN_API_KEY')
        self.wallet = os.environ.get('WALLET_ADDRESS')
        self.currencies = {"CAKE": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
                           "DIA": "0x99956D38059cf7bEDA96Ec91Aa7BB2477E0901DD"}

        self.base_chain = Bsc(host=self.host,
                              api_key=self.api_key,
                              wallet=self.wallet,
                              currencies=self.currencies)
        self.contract_address = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'

    def tearDown(self) -> None:
        del self.base_chain


class TestPolygon(unittest.TestCase, TestBaseGetRequest, TestBaseGetAccount):

    def setUp(self) -> None:
        self.name = 'POLYGON'
        self.host = 'https://api.polygonscan.com/api'
        self.api_key = os.environ.get('POLYGONSCAN_API_KEY')
        self.wallet = os.environ.get('WALLET_ADDRESS')
        self.currencies = {
            "MATIC": "0x0000000000000000000000000000000000001010"}
        self.base_chain = Polygon(host=self.host,
                                  api_key=self.api_key,
                                  wallet=self.wallet,
                                  currencies=self.currencies)
        self.contract_address = '0x0000000000000000000000000000000000001010'

    def tearDown(self) -> None:
        del self.base_chain


class TestEther(unittest.TestCase, TestBaseGetRequest, TestBaseGetAccount):

    def setUp(self) -> None:
        self.name = 'ETHER'
        self.host = 'https://api.etherscan.io/api'
        self.api_key = os.environ.get('ETHERSCAN_API_KEY')
        self.wallet = os.environ.get('WALLET_ADDRESS')
        self.currencies = {
            "ETH": "0x2170ed0880ac9a755fd29b2688956bd959f933f8"}
        self.base_chain = Ether(host=self.host,
                                api_key=self.api_key,
                                wallet=self.wallet,
                                currencies=self.currencies)
        self.contract_address = '0x2170ed0880ac9a755fd29b2688956bd959f933f8'

    def tearDown(self) -> None:
        del self.base_chain


class TestFantom(unittest.TestCase, TestBaseGetRequest, TestBaseGetAccount):

    def setUp(self) -> None:
        self.name = 'FANTOM'
        self.host = 'https://api.ftmscan.com/api'
        self.api_key = os.environ.get('FTMSCAN_API_KEY')
        self.wallet = os.environ.get('WALLET_ADDRESS')
        self.currencies = {"SAVG": "0xa097c96ACc9587D140AD8aEaAC13D9db2C6CC07f",
                           "WIS": "0xF24be6c063Bee7c7844dD90a21fdf7d783d41a94", }
        self.base_chain = Fantom(host=self.host,
                                 api_key=self.api_key,
                                 wallet=self.wallet,
                                 currencies=self.currencies)
        self.contract_address = '0xE705aF5f63fcaBDCDF5016aA838EAaac35D12890'

    def tearDown(self) -> None:
        del self.base_chain
