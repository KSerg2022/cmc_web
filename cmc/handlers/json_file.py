""""""
import os
import json
import datetime

from django.conf import settings
from pathlib import Path

base_dir = Path(__file__).parent


class JsonFile:

    def __init__(self):
        self.time_stamp = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        # self.data_dir = base_dir / 'data'
        self.data_dir = settings.BASE_DIR / 'cmc' / 'fixtures'

    def wright_data_to_json(self, data: list[dict] | dict[dict], filename):
        """Writing to file human-readable data."""
        path_to_file = self.data_dir / f'{filename}.json'
        self.check_file_exists(self.data_dir, path_to_file)

        with open(path_to_file, 'w') as file_json:
            json.dump(data, file_json, indent=4)

    def load_data_from_file(self, filename) -> dict:
        """Writing to file human-readable data."""
        # path_to_file = self.data_dir / f'{filename}.json'
        self.check_file_exists(self.data_dir, filename)
        with open(filename, 'r') as file_json:
            loaded_data = json.load(file_json)
        return loaded_data

    @staticmethod
    def check_file_exists(dir_for_file, path_to_file) -> None:
        """Check if file exists."""
        if not os.path.isdir(dir_for_file):
            os.makedirs(dir_for_file)

        if not os.path.isfile(path_to_file):
            with open(path_to_file, 'w'):
                pass

