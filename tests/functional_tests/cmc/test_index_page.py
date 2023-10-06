import time

from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.functional_tests.base import BaseTest

from cmc.models import Cryptocurrency
from cmc.fixtures.handlers.load_currencies_to_db import dump_to_db_currencies


class IndexPageTest(BaseTest):
    """test new visitor"""

    def test_index_page(self):
        dump_to_db_currencies(23)
        self.browser.get(self.live_server_url)

        current_url = self.browser.current_url
        self.assertRegex(current_url, '/')

        self.assertIn('index', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Cryptocurrencies.', header_text)

        table = self.browser.find_element(By.TAG_NAME, 'table').text
        self.assertTrue(table)

        paginate = self.browser.find_element(By.CLASS_NAME, 'pagination').text
        self.assertTrue(paginate)

        side_bar = self.browser.find_element(By.TAG_NAME, 'aside').text
        self.assertTrue(side_bar)

        side_bar_text = self.browser.find_element(By.TAG_NAME, 'h2').text
        self.assertIn('Sidebar.', side_bar_text)

        # self.assertTrue(self.get_go_back_key())

    def test_index_with_empty_db(self):
        self.browser.get(self.live_server_url)

        current_url = self.browser.current_url
        self.assertRegex(current_url, '/')
