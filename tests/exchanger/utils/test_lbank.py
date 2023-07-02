import unittest
import os
from django.test import TestCase

from exchanger.utils.ex_lbank import ExLbank

from .test_base import TestBase


class TestExLbank(TestCase, TestBase):

    def setUp(self) -> None:
        self.api_key = os.environ.get('LBANK_API_KEY')
        self.api_secret = os.environ.get('LBANK_API_SECRET_KEY')
        self.exchanger = ExLbank(api_key=self.api_key,
                                 api_secret=self.api_secret)

        self.api_key_wrong = 'wrong'
        self.api_secret_wrong = 'wrong'
        self.session = None
        self.test_data = {'result': 'true',
                          'info': {'toBtc':
                                       {'ksm': '1',
                                        'gki': '2',
                                        'sxp3s': '5',
                                        }
                                   }
                          }
        self.test_data_error = [{'error': 'currencies_account'}]

    def tearDown(self) -> None:
        del self.exchanger
