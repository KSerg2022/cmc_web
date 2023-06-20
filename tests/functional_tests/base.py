import os
import unittest
import time

# from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


MAX_WAIT = 2


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


# class BaseTest(LiveServerTestCase):
class BaseTest(StaticLiveServerTestCase):
    """test new visitor"""
    MAX_WAIT = 2

    def setUp(self) -> None:
        self.firefox_options = Options()
        self.firefox_options.add_argument("--headless")
        self.browser = webdriver.Firefox(options=self.firefox_options)

        self.user = 'user_test'
        self.first_name = 'first_name_test'
        self.email = 'test@gmail.com'
        self.password_1 = '12#$qwER'
        self.password_2 = '12#$qwER'
        self.xpath_signup = '//input[@value="Create my account"]'

    def tearDown(self) -> None:
        self.browser.quit()

    def get_username_input_box(self):
        return self.browser.find_element(By.ID, 'id_username')

    def get_first_name_input_box(self):
        return self.browser.find_element(By.ID, 'id_first_name')

    def get_email_input_box(self):
        return self.browser.find_element(By.ID, 'id_email')

    def get_password_input_box(self):
        return self.browser.find_element(By.ID, 'id_password')

    def get_password2_input_box(self):
        return self.browser.find_element(By.ID, 'id_password2')

    def press_button(self, xpath):
        return self.browser.find_element(By.XPATH, xpath).click()

    def get_sign_up_user(self):
        self.browser.find_element(By.PARTIAL_LINK_TEXT, 'Sign up').click()

        self.get_username_input_box().send_keys(self.user)
        self.get_first_name_input_box().send_keys(self.first_name)
        self.get_email_input_box().send_keys(self.email)
        self.get_password_input_box().send_keys(self.password_1)
        self.get_password2_input_box().send_keys(self.password_2)
        self.press_button(self.xpath_signup)

    def login_user(self):
        self.browser.get(self.live_server_url)
        self.get_sign_up_user()

        self.browser.find_element(By.PARTIAL_LINK_TEXT, 'Login').click()
        self.get_username_input_box().send_keys(self.user)
        self.get_password_input_box().send_keys(self.password_1)
        self.press_button(xpath='//input[@value="Log-in"]')

    def logout_user(self):
        self.browser.find_element(By.PARTIAL_LINK_TEXT, 'Logout').click()

    @wait
    def wait_for(self, fn):
        return fn()

    def get_go_back_key(self):
        return self.browser.find_element(By.XPATH, '//input[@value="« Go back!"]')
