from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
# import markdown
from django.contrib.auth.models import User

from blockchain.models import Blockchain, Portfolio
from cmc.models import Cryptocurrency

register = template.Library()


@register.simple_tag
def get_blockchain_portfolios(user):
    user = User.objects.get(id=user.id)
    user_blockchains = Portfolio.objects.filter(owner=user.id).prefetch_related('blockchain')
    return [user_blockchain.blockchain for user_blockchain in user_blockchains]


@register.simple_tag
def total_blockchain_portfolios():
    return Portfolio.objects.all().count()


@register.simple_tag
def get_sum_portfolio(portfolio):
    return round(sum([coin['total'] for coin in portfolio]), 3)

