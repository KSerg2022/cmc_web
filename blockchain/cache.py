from django.core.cache import cache

from .utils.handlers.get_data import get_data

TIME_CACHES_BLOCKCHAIN_DATA = 60*100


def check_caches_blockchain_data(portfolio):
    cache_user_blockchain = cache.get(f'user_{portfolio.owner.id}_blockchain_{portfolio.blockchain}')
    cache_user_blockchain_total_sum = cache.get(f'user_{portfolio.owner.id}_blockchain_total_sum_{portfolio.blockchain}')

    if cache_user_blockchain and cache_user_blockchain_total_sum:
        response_exchanger = cache_user_blockchain
        total_sum = cache_user_blockchain_total_sum
    else:
        response_exchanger, total_sum = get_data(portfolio)
        cache.set(f'user_{portfolio.owner.id}_blockchain_{portfolio.blockchain}',
                  response_exchanger,
                  TIME_CACHES_BLOCKCHAIN_DATA)
        cache.set(f'user_{portfolio.owner.id}_blockchain_total_sum_{portfolio.blockchain}',
                  total_sum,
                  TIME_CACHES_BLOCKCHAIN_DATA)
    return response_exchanger, total_sum
