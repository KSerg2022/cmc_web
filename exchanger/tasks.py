from django.contrib.auth.models import User

from celery import shared_task

from exchanger.utils.handlers.xlsx_file import XlsxFile


@shared_task
def save_xlsx_file(user_id, user_portfolios_data):
    user = User.objects.get(pk=user_id)
    XlsxFile(user).create_xlsx(user_portfolios_data)
