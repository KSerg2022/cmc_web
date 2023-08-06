from django.contrib.auth.models import User

from celery import shared_task

from exchanger.utils.handlers.xlsx_file import XlsxFile


@shared_task
def save_all_to_xlsx_file(user_id, user_portfolios_data, portfolio_name):
    user = User.objects.get(pk=user_id)
    XlsxFile(user, portfolio_name).create_xlsx(user_portfolios_data)


@shared_task
def save_portfolio_to_xlsx_file(user_id, user_portfolios_data, portfolio_name):
    user = User.objects.get(pk=user_id)
    XlsxFile(user, portfolio_name).create_xlsx(user_portfolios_data)

