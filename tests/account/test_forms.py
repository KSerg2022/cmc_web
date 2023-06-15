from django.test import TestCase
from django.urls import reverse

from account.forms import (LoginForm,
                           UserRegistrationForm,
                           UserEditForm,
                           ProfileEditForm,
                           EMPTY_FIELD_ERROR, VALID_ERROR)


class LoginFormTest(TestCase):

    def test_render_login_form(self):
        form = LoginForm()
        self.assertIn('name="username"', form.as_p())
        self.assertIn('name="password"', form.as_p())
        self.assertIn('placeholder="Enter a user name"', form.as_p())
        self.assertIn('placeholder="Enter a user password"', form.as_p())

    def test_form_fields_is(self):
        form = LoginForm()
        fields = ('username', 'password')
        for field in fields:
            self.assertIn(field, form.fields)

    def test_form_validation_for_blank_username(self):
        form = LoginForm(data={'username': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [EMPTY_FIELD_ERROR + '"username"'])

    def test_form_validation_for_blank_password(self):
        form = LoginForm(data={'password': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], [EMPTY_FIELD_ERROR + '"password"'])


class ProfileEditFormTest(TestCase):

    def test_render_user_edit_form(self):
        form = ProfileEditForm()
        self.assertIn('placeholder="Enter a date of birth"', form.as_p())
        self.assertIn('placeholder="Choose a user photo"', form.as_p())


class RegistrationUser(TestCase):
    def setUp(self) -> None:
        self.username = 'user_test'
        self.user_password = '!qa2ws3ED'
        self.user_email = 'test@gamil.com'
        self.user_first_name = 'user_first_name'
        self.url = reverse('register')
        self.client.post(self.url,
                         data={'username': self.username,
                               'first_name': self.user_first_name,
                               'email': self.user_email,
                               'password': self.user_password,
                               'password2': self.user_password,
                               })

        self.username2 = 'user_test2'
        self.user_password2 = '!qa2ws3ED2'
        self.user_email2 = 'test@gamil.com'
        self.user_first_name2 = 'user_first_name2'


class UserEditFormTest(RegistrationUser):

    def test_render_user_edit_form(self):
        form = UserEditForm()
        self.assertIn('placeholder="Enter a first name"', form.as_p())
        self.assertIn('placeholder="Enter a last name"', form.as_p())
        self.assertIn('placeholder="Enter a email"', form.as_p())

    def test_form_validation_for_wrong_email(self):
        form = UserEditForm(data={'email': 'wrong_email@gmail'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [VALID_ERROR + '"email"'])

    def test_form_validation_with_duplicate_email(self):
        form = UserEditForm(data={'username': self.username2,
                                  'first_name': self.user_first_name2,
                                  'email': self.user_email2,
                                  'password': self.user_password2,
                                  'password2': self.user_password2
                                  })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Email already in use.'])


class UserRegistrationFormTest(RegistrationUser):

    def test_render_user_register_form(self):
        form = UserRegistrationForm()
        self.assertIn('placeholder="Enter a user name"', form.as_p())
        self.assertIn('placeholder="Enter a last name"', form.as_p())
        self.assertIn('placeholder="Enter a email"', form.as_p())
        self.assertIn('placeholder="Enter a password"', form.as_p())
        self.assertIn('placeholder="Repeat a password"', form.as_p())

    def test_user_register_form_with_empty_username(self):
        form = UserRegistrationForm(data={'username': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [EMPTY_FIELD_ERROR + '"username"'])

    def test_user_register_form_with_wrong_email(self):
        form = UserRegistrationForm(data={'email': 'wrong_email@gmail'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [VALID_ERROR + '"email"'])

    def test_user_register_form_with_empty_password(self):
        form = UserRegistrationForm(data={'password': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], [EMPTY_FIELD_ERROR + '"password"'])

    def test_user_register_form_with_numeric_password(self):
        form = UserRegistrationForm(data={'password': '123456789'})

        self.assertFalse(form.is_valid())
        self.assertIn('This password is entirely numeric.', form.errors['password'], form.data)

    def test_user_register_form_with_shot_password(self):
        form = UserRegistrationForm(data={'password': '123'})

        self.assertFalse(form.is_valid())
        self.assertIn('This password is too short. It must contain at least 8 characters.',
                      form.errors['password'], form.data)

    def test_user_register_form_with_common_password(self):
        form = UserRegistrationForm(data={'password': '12345qwert'})

        self.assertFalse(form.is_valid())
        self.assertIn('This password is too common.', form.errors['password'], form.data)

    def test_user_register_form_with_empty_password2(self):
        form = UserRegistrationForm(data={'password2': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], [EMPTY_FIELD_ERROR + '"password"'])

    def test_user_register_form_with_not_match_password2(self):
        form = UserRegistrationForm(data={'password': '%tg6yh7UJ',
                                          'password2': '%tg6yh7UJ_'})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['Passwords don\'t match.'])

    def test_user_register_form_with_duplicate_email(self):
        form = UserRegistrationForm(data={'username': self.username2,
                                          'first_name': self.user_first_name2,
                                          'email': self.user_email2,
                                          'password': self.user_password2,
                                          'password2': self.user_password2
                                          })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Email already in use.'])
