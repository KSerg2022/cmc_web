from django import template
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils.safestring import mark_safe
# import markdown
from django.contrib.auth.models import User
from django.conf import settings



from cmc.models import Cryptocurrency

register = template.Library()

TIME_CACHE_ALL_COINS = 60*60*24


@register.simple_tag
def get_all_coins():
    cache.delete("user_all_coins")
    cache_all_coins = cache.get('user_all_coins')
    if cache_all_coins:
        coins = cache_all_coins
    else:
        try:
            coins_data = Cryptocurrency.objects.all()
        except ObjectDoesNotExist:
            return 0

        coins = {}
        for coin in coins_data:
            coins[coin.symbol] = [coin.website, coin.logo]

        cache.set('user_all_coins',
                  coins,
                  TIME_CACHE_ALL_COINS)
    return coins


# @register.simple_tag
# def total_coins():
#     return Cryptocurrency.objects.all().count()





