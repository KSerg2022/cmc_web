import json

from cmc.models import Cryptocurrency
from cmc.handlers.json_file import JsonFile
from cmc.handlers.cmc_api import Cmc


def dump_to_db(qty):
    filename = Cmc().filename
    currencies = JsonFile().load_data_from_file(filename)
    for currency in currencies[:qty]:
        Cryptocurrency.objects.update_or_create(symbol=currency['fields']['symbol'],
                                                name=currency['fields']['name'],
                                                slug=currency['fields']['slug'],
                                                website=currency['fields']['slug'],
                                                contract=currency['fields']['slug'],
                                                description=currency['fields']['slug'],
                                                logo=currency['fields']['slug']
                                                )
    # print('DB was filling')


if __name__ == '__main__':
    dump_to_db(10)
