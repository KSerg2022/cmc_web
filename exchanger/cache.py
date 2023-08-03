from django.core.cache import cache

from local_settings import TIME_CACHE_USER_PORTFOLIO_DATA, TIME_CACHES_EXCHANGER_DATA
from .utils.main.get_all_data import get_all_data
from .utils.main.get_data import get_data


def check_cache_user_portfolios_data(user_id):
    cache_user_portfolios_data = cache.get(f'user_{user_id}_portfolios_data')
    if cache_user_portfolios_data:
        user_portfolios_data = cache_user_portfolios_data
    else:
        user_portfolios_data = get_all_data(user_id)
        cache.set(f'user_{user_id}_portfolios_data',
                  user_portfolios_data,
                  TIME_CACHE_USER_PORTFOLIO_DATA)

    return user_portfolios_data


def check_caches_exchanger_data(portfolio):
    cache_user_exchanger = cache.get(f'user_{portfolio.owner.id}_exchanger_{portfolio.exchanger}')
    cache_user_cache_user_exchanger_total_sum = cache.get(
        f'user_{portfolio.owner.id}_exchanger_total_sum_{portfolio.exchanger}')

    if cache_user_exchanger and cache_user_cache_user_exchanger_total_sum:
        response_exchanger = cache_user_exchanger
        total_sum = cache_user_cache_user_exchanger_total_sum
    else:
        response_exchanger, total_sum = get_data(portfolio)
        cache.set(f'user_{portfolio.owner.id}_exchanger_{portfolio.exchanger}',
                  response_exchanger,
                  TIME_CACHES_EXCHANGER_DATA)
        cache.set(f'user_{portfolio.owner.id}_exchanger_total_sum_{portfolio.exchanger}',
                  total_sum,
                  TIME_CACHES_EXCHANGER_DATA)
    return response_exchanger, total_sum


def delete_caches_exchanger_data(portfolio):
    cache.delete(f'user_{portfolio.owner.id}_exchanger_{portfolio.exchanger}')
    cache.delete(f'user_{portfolio.owner.id}_exchanger_total_sum_{portfolio.exchanger}')
    cache.delete(f'user_{portfolio.owner.id}_exchangers')
    cache.delete('total_exchanger_portfolios')

    return


def delete_cache_user_portfolios_data(user_id):
    cache.delete(f'user_{user_id}_portfolios_data')
    return
