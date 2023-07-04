import json
from django.conf import settings
from cmc.handlers.json_file import JsonFile

from blockchain.models import Blockchain


def dump_to_db_blockchain():
    filename = settings.BASE_DIR /'blockchain'/'fixtures'/'blockchain.json'

    blockchains = JsonFile().load_data_from_file(filename)
    for blockchain in blockchains:
        Blockchain.objects.update_or_create(name=blockchain['fields']['name'],
                                            slug=blockchain['fields']['slug'],
                                            host=blockchain['fields']['host'],
                                            logo=blockchain['fields']['logo'],
                                            website=blockchain['fields']['website'],
                                            scan_site=blockchain['fields']['scan_site']
                                            )
    # print('DB was filling')