import json

from cmc.models import Cryptocurrency
from cmc.handlers.json_file import JsonFile
from cmc.handlers.cmc_api import Cmc


def dump_to_db():
    filename = Cmc().filename
    currencies = JsonFile().load_data_from_file(filename)
    # Cryptocurrency.objects.bulk_create(currencies)
    for currency in currencies:
        Cryptocurrency.objects.update_or_create(symbol=currency['symbol'],
                                                name=currency['name'],
                                                slug=currency['slug'],
                                                cmc_id=currency['cmc_id'],
                                                )
    print('DB was filling')


if __name__ == '__main__':
    dump_to_db()
