
from selenium.webdriver.common.by import By

from tests.functional_tests.base import BaseTest


class IndexPageTest(BaseTest):
    """test new visitor"""

    def test_index_page(self):
        self.browser.get(self.live_server_url)

        current_url = self.browser.current_url
        self.assertRegex(current_url, '/')

        self.assertIn('index', self.browser.title)

        # header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        # self.assertIn('You are will be happy here!', header_text)

        self.assertTrue(self.get_go_back_key())

