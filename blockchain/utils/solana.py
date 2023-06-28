"""
https://solscan.io/
"""
import os

from blockchain.utils.base import Base


class Solana(Base):
    """"""

    def __init__(self, host, api_key, wallet, currencies):
        super().__init__()
        self.host = host
        self.api_key = api_key
        self.wallet = wallet
        self.currencies = currencies
        self.headers = {
            'accept': 'application/json',
            'token': self.api_key,
        }
        self.params = {'account': self.wallet,
                       }
        self.blockchain = os.path.splitext(os.path.basename(__file__))[0]

    def get_account(self) -> dict[dict]:
        """"""
        response = self._get_request(url=self.host, params=self.params, headers=self.headers)
        if 'error' in response:
            return {self.blockchain: [response]}
        currencies = self._normalize_data(response)
        return {self.blockchain: sorted(currencies, key=lambda x: x['coin'])}

    def _normalize_data(self, currencies):
        results = []
        for currency in currencies:
            try:
                results.append({'coin': currency['tokenSymbol'],
                                'bal': int(currency['tokenAmount']['amount']) /
                                       10 ** currency['tokenAmount']['decimals']})
            except KeyError:
                if currency['tokenAddress'] in self.currencies.values():
                    for symbol, address in self.currencies.items():
                        if currency['tokenAddress'] == address:
                            results.append({'coin': symbol,
                                            'bal': int(currency['tokenAmount']['amount']) /
                                                   10 ** currency['tokenAmount']['decimals']})

        return results
