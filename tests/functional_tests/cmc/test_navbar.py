
from selenium.webdriver.common.by import By
from django.urls import reverse

from tests.functional_tests.base import BaseTest


class TestNavBar(BaseTest):

    def setUp(self) -> None:
        super(TestNavBar, self).setUp()
        self.live_server_url = self.live_server_url

    def test_check_nav_bar_before_login(self):
        self.browser.get(self.live_server_url)
        nav_bar_before_login = self.browser.find_element(By.TAG_NAME, 'nav').text

        self.assertIn('Home', nav_bar_before_login)
        # self.assertIn('?', nav_bar_before_login)  # todo - add late menu
        # self.assertIn('?', nav_bar_before_login)  # todo - add late menu
        self.assertIn('Login', nav_bar_before_login)
        self.assertIn('Sign up', nav_bar_before_login)

    def test_check_nav_bar_after_login(self):
        self.browser.get(self.live_server_url)
        self.login_user()
        nav_bar_after_login = self.browser.find_element(By.TAG_NAME, 'nav').text

        self.assertTrue(nav_bar_after_login)
        self.assertIn('Home', nav_bar_after_login)
        # self.assertIn('?', nav_bar_after_login)  # todo - add late menu
        # self.assertIn('?', nav_bar_after_login)  # todo - add late menu
        self.assertIn(f'Hello, ', nav_bar_after_login)

        self.assertIn('Settings', nav_bar_after_login)
        self.assertIn('Logout', nav_bar_after_login)

        self.assertNotIn('Login', nav_bar_after_login)
        self.assertNotIn('Sign up', nav_bar_after_login)

