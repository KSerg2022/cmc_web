from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
# import markdown
from django.contrib.auth.models import User

from exchanger.models import Exchanger, ExPortfolio
from cmc.models import Cryptocurrency

register = template.Library()


@register.simple_tag
def get_exchanger_portfolios(user):
    user = User.objects.get(id=user.id)
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
    return round(sum([coin['total'] for coin in portfolio]), 3)


# @register.inclusion_tag('blog/latest_posts.html')
# def show_latest_posts(count=5):
#     latest_posts = Post.objects.filter(status='published').order_by('-publish')[:count]
#     if not latest_posts:
#         return {'latest_posts': ''}
#     return {'latest_posts': latest_posts}

#
# @register.simple_tag
# def get_most_commented_posts(count=5):
#     return Post.objects.filter(status='published').annotate(
#         total_comments=Count('comments')
#     ).order_by('-total_comments')[:count]




# @register.simple_tag
# def total_user_posts(user=None):
#     return Post.objects.filter(author=user).count()
#
#
# @register.simple_tag
# def total_user_posts_with_status(user=None, status=None):
#     return Post.objects.filter(status=status).filter(author=user).count()
