import time

from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.functional_tests.base import BaseTest

from cmc.models import Cryptocurrency
from cmc.utils.load_data_to_db import dump_to_db


class DetailPageTest(BaseTest):
    """test new visitor"""

    def test_detail_page(self):
        dump_to_db(3)
        crypto = 'Litecoin'
        self.browser.get(self.live_server_url)
        q = self.browser.find_element(By.PARTIAL_LINK_TEXT, crypto).click()

        current_url = self.browser.current_url
        self.assertRegex(current_url, f'/cmc/detail/{crypto.lower()}/')

        self.wait_for(lambda: self.assertIn('detail_crypto', self.browser.title))

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(crypto, header_text)

        table = self.browser.find_element(By.TAG_NAME, 'table').text
        self.assertTrue(table)

        side_bar = self.browser.find_element(By.TAG_NAME, 'aside').text
        self.assertTrue(side_bar)

        side_bar_text = self.browser.find_element(By.TAG_NAME, 'h2').text
        self.assertIn('Sidebar.', side_bar_text)

        self.assertTrue(self.get_go_back_key())

