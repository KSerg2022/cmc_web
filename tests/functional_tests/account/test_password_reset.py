import re

from django.core import mail
from selenium.webdriver.common.by import By
from django.urls import reverse

from tests.functional_tests.base import BaseTest


class TestPasswordReset(BaseTest):

    def setUp(self) -> None:
        super(TestPasswordReset, self).setUp()
        # self.live_server_url = self.live_server_url + reverse('login')

    def signup_and_goto_page_login(self):
        self.browser.get(self.live_server_url)
        self.get_sign_up_user()

        self.browser.find_element(By.PARTIAL_LINK_TEXT, 'Login').click()

    def test_forgotten_your_password(self):
        self.signup_and_goto_page_login()
        self.browser.find_element(By.PARTIAL_LINK_TEXT, 'Forgotten your password?').click()

        current_url = self.browser.current_url
        self.assertRegex(current_url, reverse('password_reset'))

        self.assertIn('Reset your password', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(f'Forgotten your password?', header_text)

        p_text = self.browser.find_element(By.TAG_NAME, 'p').text
        self.assertEqual("Enter your e-mail address to obtain a new password.",
                         p_text)
        login_key = self.browser.find_element(By.XPATH, '//input[@value="Send e-mail"]')
        self.assertTrue(login_key)

        self.assertTrue(self.get_go_back_key())

    def test_send_email(self):
        self.signup_and_goto_page_login()
        self.browser.find_element(By.PARTIAL_LINK_TEXT, 'Forgotten your password?').click()

        self.get_email_input_box().send_keys(self.email)
        self.press_button('//input[@value="Send e-mail"]')

        current_url = self.browser.current_url
        self.assertRegex(current_url, reverse('password_reset_done'))

        self.assertIn('Reset your password', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(f'Reset your password', header_text)

        p_text = self.browser.find_element(By.TAG_NAME, 'p').text
        self.assertEqual("We've emailed you instructions for setting your password.",
                         p_text)

        self.assertTrue(self.get_go_back_key())

    def test_goto_by_link_in_email(self):
        self.signup_and_goto_page_login()
        self.browser.find_element(By.PARTIAL_LINK_TEXT, 'Forgotten your password?').click()

        self.get_email_input_box().send_keys(self.email)
        self.press_button('//input[@value="Send e-mail"]')

        body_email = mail.outbox[0].body
        url_for_reset_password = re.search(r'(http|https)://.*', body_email).group()

        self.browser.get(url_for_reset_password)

        self.assertIn('Reset your password', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(f'Reset your password', header_text)

        p_text = self.browser.find_element(By.TAG_NAME, 'p').text
        self.assertEqual("Please enter your new password twice:",
                         p_text)

        change_my_password_key = self.browser.find_element(By.XPATH, '//input[@value="Change my password"]')
        self.assertTrue(change_my_password_key)

        self.assertTrue(self.get_go_back_key())

    def test_enter_new_password(self):
        self.signup_and_goto_page_login()
        self.browser.find_element(By.PARTIAL_LINK_TEXT, 'Forgotten your password?').click()

        self.get_email_input_box().send_keys(self.email)
        self.press_button('//input[@value="Send e-mail"]')

        body_email = mail.outbox[0].body
        url_for_reset_password = re.search(r'(http|https)://.*', body_email).group()
        self.browser.get(url_for_reset_password)

        self.browser.find_element(By.ID, 'id_new_password1').send_keys('98#$qwER')
        self.browser.find_element(By.ID, 'id_new_password2').send_keys('98#$qwER')

        self.browser.find_element(By.XPATH, '//input[@value="Change my password"]').click()

        self.assertIn('Password reset', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(f'Password set', header_text)

        p_text = self.browser.find_element(By.TAG_NAME, 'p').text
        self.assertEqual("Your password has been set. You can log in now",
                         p_text)

        self.assertTrue(self.get_go_back_key())
