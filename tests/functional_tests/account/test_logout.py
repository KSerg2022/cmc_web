
from selenium.webdriver.common.by import By
from django.urls import reverse

from tests.functional_tests.base import BaseTest


class TestLogoutPage(BaseTest):

    def setUp(self) -> None:
        super(TestLogoutPage, self).setUp()
        self.live_server_url = self.live_server_url + reverse('logout')

    def test_logout_page(self):
        self.browser.get(self.live_server_url)
        self.login_user()
        self.logout_user()

        self.assertIn('Logged out', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(f'Logged out', header_text)

        p_text = self.browser.find_element(By.TAG_NAME, 'p').text
        self.assertEqual("You have been successfully logged out. You can log-in again.",
                         p_text)

        self.assertTrue(self.get_go_back_key())
