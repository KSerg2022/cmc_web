from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils.safestring import mark_safe
# import markdown
from django.contrib.auth.models import User
from django.core.cache import cache

from blockchain.models import Blockchain, Portfolio
from cmc.models import Cryptocurrency

register = template.Library()

TIME_CACHES_DATA = 60*10


@register.simple_tag
def get_blockchain_portfolios(user):
    cache_user_blockchains = cache.get(f'user_{user.id}_blockchains')
    if cache_user_blockchains:
        blockchains = cache_user_blockchains
    else:
        try:
            user = User.objects.get(id=user.id)
        except ObjectDoesNotExist:
            return 0
        user_blockchains = Portfolio.objects.filter(owner=user.id).prefetch_related('blockchain')
        blockchains = [user_blockchain.blockchain for user_blockchain in user_blockchains]
        cache.set(f'user_{user.id}_blockchains', blockchains, TIME_CACHES_DATA)
    return blockchains


@register.simple_tag
def total_blockchain_portfolios():
    cache_total_blockchain_portfolios = cache.get('total_blockchain_portfolios')
    if cache_total_blockchain_portfolios:
        qty_blockchain_portfolios = cache_total_blockchain_portfolios
    else:
        qty_blockchain_portfolios = Portfolio.objects.all().count()
        cache.set('total_blockchain_portfolios', qty_blockchain_portfolios, TIME_CACHES_DATA)
    return qty_blockchain_portfolios


@register.simple_tag
def get_sum_portfolio(portfolio):
    return round(sum([coin['total'] for coin in portfolio]), 3)

