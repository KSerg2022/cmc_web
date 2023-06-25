"""
https://bscscan.com/
"""
import os

from blockchain.utils.base import Base


class Bsc(Base):
    """"""

    def __init__(self, api_key, wallet, currencies):
        super().__init__()
        self.host = 'https://api.bscscan.com/api'
        self.api_key = api_key
        self.wallet = wallet
        self.currencies = currencies
        self.params = {'module': 'account',
                       'action': 'tokenbalance',
                       'contractaddress': '',
                       'address': self.wallet,
                       'tag': 'latest',
                       'apikey': self.api_key,
                       }
        self.blockchain = os.path.splitext(os.path.basename(__file__))[0]

