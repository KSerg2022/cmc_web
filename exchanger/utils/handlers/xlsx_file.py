""""""
import os
import pandas as pd

from django.conf import settings


class XlsxFile:

    def __init__(self, user):
        self.dir = settings.MEDIA_ROOT / 'xlsx_files' / f'{user.id}_{user.username.lower()}'
        self.filename = f'{user.id}_{user.username.lower()}.xlsx'
        self.path_to_file = self.dir / self.filename

    def create_xlsx(self, data: list[dict]):
        data = sorted(data, key=lambda x: len(list(x.values())[0]), reverse=True)
        self.check_file_exists()
        table, headers_lines, headers_columns = self.create_table(data)
        self.create_xlsx_file(table, headers_lines, headers_columns)

    def create_xlsx_file(self, table: list[list], line_index: list[dict], columns: list[str]):
        """"""
        df = pd.DataFrame(table, index=line_index, columns=columns)
        df.to_excel(self.path_to_file, sheet_name='Sheet1', startrow=0, startcol=0)

    def create_table(self, data: list[dict]):
        table = []
        headers_lines = []
        for exchanger in data:
            for currency in list(exchanger.values())[0]:
                row = list(currency.values())
                table.append(row)

                headers_lines.append(list(exchanger.keys())[0])
        headers_columns = list(list(data[0].values())[0][0].keys())
        return table, headers_lines, headers_columns

    def check_file_exists(self) -> None:
        """Check if file exists."""
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)

        if not os.path.isfile(self.path_to_file):
            with open(self.path_to_file, 'w'):
                pass