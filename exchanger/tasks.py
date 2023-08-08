from __future__ import absolute_import, unicode_literals
import os

from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404

from core.settings import BASE_DIR

from celery import shared_task

from exchanger.utils.handlers.xlsx_file import XlsxFile

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


@shared_task()
def sending_email(user_id, path_to_file):
    if not path_to_file:
        return {"error": "File not created yet", "status": 400}

    from django.contrib.auth.models import User
    user = get_object_or_404(User,
                             id=user_id)
    if not (email := user.email):
        return {"error": "You have not added an email to your registration details", "status": 400}

    subject = f'All portfolios data for user - {user.username}'
    message = f'Dear {user.username},\n\n' \
              f'This letter contains information about your Portfolios. XLSX.'
    msg = EmailMessage(subject,
                       message,
                       os.environ.get('EMAIL'),
                       [email])
    msg.attach_file(str(BASE_DIR) + path_to_file, mimetype='text/*')
    try:
        msg.send()
    except BadHeaderError:
        return {"error": "Invalid header found.", "status": 400}
    return {"message": "Successful", "status": 200}


@shared_task()
def sending_PDF_by_email(user_id, path_to_file=None, portfolio=None):
    from django.contrib.auth.models import User
    from exchanger.cache import check_cache_user_portfolios_data, check_caches_exchanger_data
    from blockchain.cache import check_caches_blockchain_data
    from exchanger.views import get_pdf, get_exchanger_pdf
    from django.core.exceptions import ObjectDoesNotExist
    from .models import ExPortfolio
    from blockchain.models import Portfolio

    user = get_object_or_404(User, id=user_id)
    if not (email := user.email):
        return {"error": "You have not added an email to your registration details", "status": 400}

    subject = f'Portfolio {portfolio} data for user - {user.username}'
    message = f'Dear {user.username},\n\n' \
              f'This letter contains information about your Portfolios. PDF.'
    msg = EmailMessage(subject,
                       message,
                       os.environ.get('EMAIL'),
                       [email])
    if portfolio:
        try:
            portfolio = ExPortfolio.objects.get(owner=user,
                                                exchanger__slug=portfolio.lower())
            response, total_sum = check_caches_exchanger_data(portfolio)
        except (ValueError, ObjectDoesNotExist):
            portfolio = Portfolio.objects.get(owner=user,
                                              blockchain__slug=portfolio.lower())
            response, total_sum = check_caches_blockchain_data(portfolio)
        pdf = get_exchanger_pdf(portfolio, response, total_sum)

    else:
        user_portfolios_data = check_cache_user_portfolios_data(user_id)
        pdf = get_pdf(user_portfolios_data)

    path_to_file = str(BASE_DIR) + path_to_file
    with open(path_to_file, 'wb') as f:
        f.write(pdf)
    msg.attach_file(path_to_file, mimetype='text/*')
    try:
        msg.send()
    except BadHeaderError:
        return {"error": "Invalid header found.", "status": 400}
    return {"message": "Successful", "status": 200}
