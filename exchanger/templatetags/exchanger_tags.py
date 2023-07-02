from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils.safestring import mark_safe
# import markdown
from django.contrib.auth.models import User
from django.conf import settings


from exchanger.models import Exchanger, ExPortfolio
from cmc.models import Cryptocurrency

register = template.Library()


@register.simple_tag
def get_exchanger_portfolios(user):
    try:
        user = User.objects.get(id=user.id)
    except ObjectDoesNotExist:
        return 0
    user_exchangers = ExPortfolio.objects.filter(owner=user.id).prefetch_related('exchanger')

    return [user_exchanger.exchanger for user_exchanger in user_exchangers]


@register.simple_tag
def total_coins():
    return Cryptocurrency.objects.all().count()


@register.simple_tag
def total_users():
    return User.objects.all().count()


@register.simple_tag
def total_exchanger_portfolios():
    return ExPortfolio.objects.all().count()


@register.simple_tag
def get_sum_portfolio(portfolio):
    return round(sum([coin['total'] for coin in portfolio if 'total' in coin]), 3)


@register.simple_tag
def get_path_to_users_xlsx_file(user):
    xlsx_dir = settings.MEDIA_URL + 'xlsx_files/' + f'{user.id}_{user.username.lower()}/'
    filename = f'{user.id}_{user.username.lower()}.xlsx'
    path_to_file = xlsx_dir + filename
    return path_to_file


