import os
from unittest import skip
import time

# from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from tests.functional_tests.base import BaseTest


class TestSignUpPage(BaseTest):

    def setUp(self) -> None:
        super(TestSignUpPage, self).setUp()
        self.live_server_url = self.live_server_url + reverse('register')

    def test_sign_up_user(self):
        self.browser.get(self.live_server_url)
        self.get_sign_up_user()

        current_url = self.browser.current_url
        self.assertRegex(current_url, '/')
        self.assertIn('Welcome', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(f'Welcome {self.first_name}!', header_text)

        p_text = self.browser.find_element(By.TAG_NAME, 'p').text
        self.assertEqual('Your account has been successfully created. Now you can log in.',
                         p_text)
        login = self.browser.find_element(By.LINK_TEXT, 'log in').text
        self.assertEqual('log in', login)

    def test_signup_with_not_correct_data(self):
        self.browser.get(self.live_server_url)

        self.get_username_input_box().send_keys(self.user)
        self.get_password_input_box().send_keys(self.password_1)
        self.get_password2_input_box().send_keys('12#$qwER_')
        self.press_button(self.xpath_signup)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.errorlist').text,
            "Passwords don't match."))

        current_url = self.browser.current_url
        self.assertRegex(current_url, '/account/register/')

        self.assertIn('Create an account', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Create an account', header_text)

        inputs = self.browser.find_elements(By.TAG_NAME, 'input')
        # self.assertIn('« Go back!', [input_.get_attribute("value") for input_ in inputs])
        self.assertIn('Create my account', [input_.get_attribute("value") for input_ in inputs])

    def test_signup_with_empty_username(self):
        self.browser.get(self.live_server_url)
        self.press_button(self.xpath_signup)

        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_username:invalid'))

    def test_csignup_with_empty_password(self):
        self.browser.get(self.live_server_url)
        self.get_username_input_box().send_keys(self.user)
        self.press_button(self.xpath_signup)

        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_username:valid'))
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_password:invalid'))

    def test_signup_with_empty_password2(self):
        self.browser.get(self.live_server_url)
        self.get_username_input_box().send_keys(self.user)
        self.get_password_input_box().send_keys(self.password_1)
        self.press_button(self.xpath_signup)

        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_username:valid'))
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_password:valid'))
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_password2:invalid'))

    def test_signup_add_duplicate_user(self):
        self.browser.get(self.live_server_url)
        self.get_sign_up_user()
        # self.logout_user()

        self.browser.get(self.live_server_url)
        self.get_sign_up_user()

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.errorlist').text,
            "A user with that username already exists."))

