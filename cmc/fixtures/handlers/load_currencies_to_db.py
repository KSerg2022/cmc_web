from django.conf import settings

from cmc.handlers.json_file import JsonFile

from cmc.models import Cryptocurrency
from cmc.handlers.cmc_api import Cmc


def dump_to_db_currencies(qty):
    filename = settings.BASE_DIR /'blockchain'/'fixtures'/'cryptocurrency.json'
    currencies = JsonFile().load_data_from_file(filename)
    for currency in currencies[:qty]:
        Cryptocurrency.objects.update_or_create(symbol=currency['fields']['symbol'],
                                                name=currency['fields']['name'],
                                                slug=currency['fields']['slug'],
                                                website=currency['fields']['website'],
                                                contract=currency['fields']['contract'],
                                                description=currency['fields']['description'],
                                                logo=currency['fields']['logo']
                                                )
    # print('DB was filling')
