
from celery import shared_task

from django.conf import settings
from django.core.cache import cache
from django.db import transaction

from cmc.handlers.json_file import JsonFile
from cmc.handlers.cmc_fixtires import Cmc


from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
@shared_task
def sample_task():
    logger.info("1------------------- 1 -------------- The sample task just ran.")


@shared_task()
def cmc_currencies():
    result = Cmc()
    result.get_cryptocurrency()

    cache.delete("user_all_coins")
    dump_to_db_currencies()


def dump_to_db_currencies():
    filename = settings.BASE_DIR / 'cmc' / 'fixtures' / 'cryptocurrency.json'
    currencies = JsonFile().load_data_from_file(filename)
    from cmc.models import Cryptocurrency

    with transaction.atomic():
        for currency in currencies:
            data = {'symbol': currency['fields']['symbol'],
                    'name': currency['fields']['name'],
                    'slug': currency['fields']['slug'],
                    'website': currency['fields']['website'],
                    'contract': currency['fields']['contract'],
                    'description': currency['fields']['description'],
                    'logo': currency['fields']['logo']
                    }
            obj, created = Cryptocurrency.objects.update_or_create(slug=currency['fields']['slug'], defaults=data)
