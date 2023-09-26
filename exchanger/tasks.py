from __future__ import absolute_import, unicode_literals
import os

from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404

from django.conf import settings

from celery import shared_task

from exchanger.utils.handlers.xlsx_file import XlsxFile
from local_settings import ALL_PORTFOLIOS

from dotenv import load_dotenv

load_dotenv()


@shared_task
def save_all_to_xlsx_file(user_id, user_portfolios_data, portfolio_name):
    from django.contrib.auth.models import User

    user = User.objects.get(pk=user_id)
    XlsxFile(user, portfolio_name).create_xlsx(user_portfolios_data)


@shared_task
def save_portfolio_to_xlsx_file(user_id, user_portfolios_data, portfolio_name):
    from django.contrib.auth.models import User

    user = User.objects.get(pk=user_id)
    XlsxFile(user, portfolio_name).create_xlsx(user_portfolios_data)


def get_portfolio_data(user, portfolio):
    from exchanger.cache import check_caches_exchanger_data
    from blockchain.cache import check_caches_blockchain_data
    from django.core.exceptions import ObjectDoesNotExist
    from .models import ExPortfolio
    from blockchain.models import Portfolio

    try:
        portfolio = ExPortfolio.objects.get(owner=user,
                                            exchanger__slug=portfolio.lower())
        user_portfolios_data, total_sum = check_caches_exchanger_data(portfolio)
    except (ValueError, ObjectDoesNotExist):
        portfolio = Portfolio.objects.get(owner=user,
                                          blockchain__slug=portfolio.lower())
        user_portfolios_data, total_sum = check_caches_blockchain_data(portfolio)
    return user_portfolios_data, total_sum, portfolio


@shared_task()
def sending_XLSX_by_email(user_id, path_to_file, portfolio):
    from django.contrib.auth.models import User
    user = get_object_or_404(User,
                             id=user_id)
    if not (email := user.email):
        return {"error": "You have not added an email to your registration details", "status": 400}

    subject = f'Portfolio {portfolio} data for user in xlsx-file - {user.username}'
    message = f'Dear {user.username},\n\n' \
              f'This letter contains information about your Portfolios. XLSX.'
    msg = EmailMessage(subject,
                       message,
                       os.environ.get('EMAIL'),
                       [email])

    from exchanger.cache import check_cache_user_portfolios_data

    if portfolio != ALL_PORTFOLIOS:
        user_portfolios_data, total_sum, _ = get_portfolio_data(user, portfolio)
        save_portfolio_to_xlsx_file(user_id,
                                    [{portfolio: user_portfolios_data}],
                                    portfolio)
    else:
        user_portfolios_data = check_cache_user_portfolios_data(user_id)
        save_all_to_xlsx_file(user_id, user_portfolios_data, portfolio_name=ALL_PORTFOLIOS)

    msg.attach_file(str(settings.BASE_DIR) + path_to_file, mimetype='text/*')
    try:
        msg.send()
    except BadHeaderError:
        return {"error": "Invalid header found.", "status": 400}
    return {"message": "Successful", "status": 200}


@shared_task()
def sending_PDF_by_email(user_id, path_to_file, portfolio):
    from django.contrib.auth.models import User
    from exchanger.cache import check_cache_user_portfolios_data
    from exchanger.views import get_pdf, get_exchanger_pdf

    user = get_object_or_404(User, id=user_id)
    if not (email := user.email):
        return {"error": "You have not added an email to your registration details", "status": 400}

    subject = f'Portfolio {portfolio} data for user in pdf-file - {user.username}'
    message = f'Dear {user.username},\n\n' \
              f'This letter contains information about your Portfolios. PDF.'
    msg = EmailMessage(subject,
                       message,
                       os.environ.get('EMAIL'),
                       [email])
    if portfolio != ALL_PORTFOLIOS:
        user_portfolios_data, total_sum, portfolio_obj = get_portfolio_data(user, portfolio)
        pdf = get_exchanger_pdf(portfolio_obj, user_portfolios_data, total_sum)

    else:
        user_portfolios_data = check_cache_user_portfolios_data(user_id)
        pdf = get_pdf(user_portfolios_data)

    path_to_file = str(settings.BASE_DIR) + path_to_file
    with open(path_to_file, 'wb') as f:
        f.write(pdf)
    msg.attach_file(path_to_file, mimetype='text/*')
    try:
        msg.send()
    except BadHeaderError:
        return {"error": "Invalid header found.", "status": 400}
    return {"message": "Successful", "status": 200}
