from django import template
from django.core.exceptions import ObjectDoesNotExist

# import markdown
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache

from exchanger.models import ExPortfolio
from cmc.models import Cryptocurrency
from local_settings import TIME_CACHES_DATA, TIME_CACHES_COINS, TIME_CACHES_USERS, ALL_PORTFOLIOS

register = template.Library()


@register.simple_tag
def get_exchanger_portfolios(user):
    cache_user_exchangers = cache.get(f'user_{user.id}_exchangers')
    if cache_user_exchangers:
        exchangers = cache_user_exchangers
    else:
        try:
            user = User.objects.get(id=user.id)
            user_exchangers = ExPortfolio.objects.filter(owner=user.id).prefetch_related('exchanger')
        except ObjectDoesNotExist:
            return 0

        exchangers = [user_exchanger.exchanger for user_exchanger in user_exchangers]
        cache.set(f'user_{user.id}_exchangers', exchangers, TIME_CACHES_DATA)
    return exchangers


@register.simple_tag
def total_coins():
    cache_total_coins = cache.get('total_coins')
    if cache_total_coins:
        coins = cache_total_coins
    else:
        try:
            coins = Cryptocurrency.objects.all().count()
            cache.set('total_coins', coins, TIME_CACHES_COINS)
        except ObjectDoesNotExist:
            return 0
    return coins


@register.simple_tag
def total_users():
    cache_total_users = cache.get('total_users')
    if cache_total_users:
        qty_users = cache_total_users
    else:
        try:
            qty_users = User.objects.all().count()
            cache.set('total_users', qty_users, TIME_CACHES_USERS)
        except ObjectDoesNotExist:
            return 0
    return qty_users


@register.simple_tag
def total_exchanger_portfolios():
    cache_total_exchanger_portfolios = cache.get('total_exchanger_portfolios')
    if cache_total_exchanger_portfolios:
        qty_exchanger_portfolios = cache_total_exchanger_portfolios
    else:
        try:
            qty_exchanger_portfolios = ExPortfolio.objects.all().count()
            cache.set('total_exchanger_portfolios', qty_exchanger_portfolios, TIME_CACHES_DATA)
        except ObjectDoesNotExist:
            return 0
    return qty_exchanger_portfolios


@register.simple_tag
def get_sum_portfolio(portfolio):
    return round(sum([coin['total'] for coin in portfolio if 'total' in coin]), 5)


@register.simple_tag
def get_path_to_users_xlsx_file_all(user):
    xlsx_dir = settings.MEDIA_URL + 'xlsx_files/' + f'{user.id}_{user.username.lower()}/'
    filename = f'{user.id}_{user.username.lower()}_{ALL_PORTFOLIOS}.xlsx'
    path_to_file = xlsx_dir + filename
    return path_to_file


# вызывается каждый раз при загрузке страници - не правильно. При первом запуске, когда без кеша, долго грущится
# @register.simple_tag
# def get_path_to_users_xlsx_file_all(user, portfolio_name=ALL_PORTFOLIOS):
#     xlsx_file = XlsxFile(user, portfolio_name)
#     if os.path.isfile(xlsx_file.path_to_file):
#         return xlsx_file.path_to_file
#
#     user_portfolios_data = check_cache_user_portfolios_data(user.id)
#     save_all_to_xlsx_file.delay(user.id, user_portfolios_data, portfolio_name)
#     return xlsx_file.path_to_file


@register.simple_tag
def get_path_to_users_xlsx_file_one(user, portfolio):
    xlsx_dir = settings.MEDIA_URL + 'xlsx_files/' + f'{user.id}_{user.username.lower()}/'
    filename = f'{user.id}_{user.username.lower()}_{portfolio}.xlsx'
    path_to_file = xlsx_dir + filename
    return path_to_file
