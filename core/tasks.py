import os
import time
from django.conf import settings

from celery import shared_task

from local_settings import FILE_AGE_IN_MINUTES


@shared_task
def del_old_files_in_media_xlsx_files():
    """"""
    for (root, dirs, files) in os.walk(settings.MEDIA_ROOT / 'xlsx_files', topdown=True):
        for f in files:
            file_path = os.path.join(root, f)
            timestamp_of_file = os.path.getmtime(file_path)
            if (time.time() - timestamp_of_file) > FILE_AGE_IN_MINUTES:
                os.remove(file_path)
