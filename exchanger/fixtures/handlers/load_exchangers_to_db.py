import json
from django.conf import settings
from cmc.handlers.json_file import JsonFile

from exchanger.models import Exchanger


def dump_to_db_exchanger():
    filename = settings.BASE_DIR /'exchanger'/'fixtures'/'exchanger.json'

    exchangers = JsonFile().load_data_from_file(filename)
    for exchanger in exchangers:
        Exchanger.objects.update_or_create(name=exchanger['fields']['name'],
                                           slug=exchanger['fields']['slug'],
                                           host=exchanger['fields']['host'],
                                           url=exchanger['fields']['url'],
                                           prefix=exchanger['fields']['prefix'],
                                           logo=exchanger['fields']['logo'],
                                           website=exchanger['fields']['website'],
                                           )
    # print('DB was filling')