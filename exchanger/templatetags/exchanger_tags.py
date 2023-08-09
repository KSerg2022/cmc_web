from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils.safestring import mark_safe
# import markdown
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache

from exchanger.models import Exchanger, ExPortfolio
from cmc.models import Cryptocurrency
from local_settings import TIME_CACHES_DATA, TIME_CACHES_COINS, TIME_CACHES_USERS

register = template.Library()


@register.simple_tag
def get_exchanger_portfolios(user):
    cache_user_exchangers = cache.get(f'user_{user.id}_exchangers')
    if cache_user_exchangers:
        exchangers = cache_user_exchangers
    else:
        try:
            user = User.objects.get(id=user.id)
        except ObjectDoesNotExist:
            return 0
        user_exchangers = ExPortfolio.objects.filter(owner=user.id).prefetch_related('exchanger')
        exchangers = [user_exchanger.exchanger for user_exchanger in user_exchangers]
        cache.set(f'user_{user.id}_exchangers', exchangers, TIME_CACHES_DATA)
    return exchangers


@register.simple_tag
def total_coins():
    cache_total_coins = cache.get('total_coins')
    if cache_total_coins:
        coins = cache_total_coins
    else:
        coins = Cryptocurrency.objects.all().count()
        cache.set('total_coins', coins, TIME_CACHES_COINS)
    return coins


@register.simple_tag
def total_users():
    cache_total_users = cache.get('total_users')
    if cache_total_users:
        qty_users = cache_total_users
    else:
        qty_users = User.objects.all().count()
        cache.set('total_users', qty_users, TIME_CACHES_USERS)
    return qty_users


@register.simple_tag
def total_exchanger_portfolios():
    cache_total_exchanger_portfolios = cache.get('total_exchanger_portfolios')
    if cache_total_exchanger_portfolios:
        qty_exchanger_portfolios = cache_total_exchanger_portfolios
    else:
        qty_exchanger_portfolios = ExPortfolio.objects.all().count()
        cache.set('total_exchanger_portfolios', qty_exchanger_portfolios, TIME_CACHES_DATA)
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


@register.simple_tag
def get_path_to_users_xlsx_file_one(user, portfolio):
    xlsx_dir = settings.MEDIA_URL + 'xlsx_files/' + f'{user.id}_{user.username.lower()}/'
    filename = f'{user.id}_{user.username.lower()}_{portfolio}.xlsx'
    path_to_file = xlsx_dir + filename
    return path_to_file
