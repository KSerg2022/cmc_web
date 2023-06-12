
from selenium.webdriver.common.by import By
from django.urls import reverse

from tests.functional_tests.base import BaseTest


class TestFooter(BaseTest):

    def setUp(self) -> None:
        super(TestFooter, self).setUp()
        self.live_server_url = self.live_server_url

    def test_check_nav_bar_before_login(self):
        self.browser.get(self.live_server_url)
        footer = self.browser.find_element(By.TAG_NAME, 'footer').text

        self.assertIn('All rights reserved', footer)
        self.assertIn('Home', footer)
        # self.assertIn('?', footer)  # todo - add late menu
        # self.assertIn('?', footer)  # todo - add late menu
        # self.assertIn('?', footer)  # todo - add late menu

        self.assertTrue(self.browser.find_element(By.CSS_SELECTOR, '.fa-twitter'))
        self.assertTrue(self.browser.find_element(By.CSS_SELECTOR, '.fa-facebook'))
        self.assertTrue(self.browser.find_element(By.CSS_SELECTOR, '.fa-dropbox'))
        self.assertTrue(self.browser.find_element(By.CSS_SELECTOR, '.fa-flickr'))
        self.assertTrue(self.browser.find_element(By.CSS_SELECTOR, '.fa-github'))
        self.assertTrue(self.browser.find_element(By.CSS_SELECTOR, '.fa-linkedin'))
        self.assertTrue(self.browser.find_element(By.CSS_SELECTOR, '.fa-instagram'))
        self.assertTrue(self.browser.find_element(By.CSS_SELECTOR, '.fa-google-plus'))
