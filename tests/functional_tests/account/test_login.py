
from selenium.webdriver.common.by import By
from django.urls import reverse

from tests.functional_tests.base import BaseTest


class TestLoginPage(BaseTest):

    def setUp(self) -> None:
        super(TestLoginPage, self).setUp()
        self.live_server_url = self.live_server_url + reverse('login')

    def check_result_login_with_wrong_data(self):
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.errorlist').text,
            "Please enter a correct username and password. "
            "Note that both fields may be case-sensitive."))

        current_url = self.browser.current_url
        self.assertRegex(current_url, reverse('login'))

        self.assertIn('Log-in', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(f'Log-in', header_text)

        login_key = self.browser.find_element(By.XPATH, '//input[@value="Log-in"]')
        self.assertTrue(login_key)

    def signup_and_goto_page_login(self):
        self.browser.get(self.live_server_url)
        self.get_sign_up_user()

        self.browser.find_element(By.PARTIAL_LINK_TEXT, 'Login').click()

    def test_login_page(self):
        self.browser.get(self.live_server_url)

        self.assertIn('Log-in', self.browser.title)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(f'Log-in', header_text)

        p_text = self.browser.find_element(By.TAG_NAME, 'p').text
        self.assertEqual("Please, use the following form to log-in. If you don't have an account register here.",
                         p_text)
        login_key = self.browser.find_element(By.XPATH, '//input[@value="Log-in"]')
        self.assertTrue(login_key)

        self.assertTrue(self.get_go_back_key())

    def test_login_user(self):
        self.browser.get(self.live_server_url)
        self.login_user()

        current_url = self.browser.current_url
        self.assertRegex(current_url, '/')
        self.assertIn('index', self.browser.title)

        # header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        # self.assertIn(f'Welcome {self.first_name}!', header_text)

        # p_text = self.browser.find_element(By.TAG_NAME, 'p').text
        # self.assertEqual('Your account has been successfully created. Now you can log in.',
        #                  p_text)
        self.assertTrue(self.get_go_back_key())

    def test_login_with_not_correct_username(self):
        self.signup_and_goto_page_login()

        self.get_username_input_box().send_keys('user_wrong')
        self.get_password_input_box().send_keys(self.password_1)
        self.press_button('//input[@value="Log-in"]')

        self.check_result_login_with_wrong_data()

    def test_login_with_not_correct_password(self):
        self.signup_and_goto_page_login()

        self.get_username_input_box().send_keys(self.user)
        self.get_password_input_box().send_keys('12#$qwER_')
        self.press_button('//input[@value="Log-in"]')

        self.check_result_login_with_wrong_data()

    def test_login_with_empty_username(self):
        self.signup_and_goto_page_login()

        self.press_button('//input[@value="Log-in"]')

        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_username:invalid'))

    def test_login_with_empty_password(self):
        self.signup_and_goto_page_login()

        self.get_username_input_box().send_keys(self.user)
        self.press_button('//input[@value="Log-in"]')

        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_username:valid'))
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_password:invalid'))



