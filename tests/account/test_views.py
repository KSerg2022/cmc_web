from django.test import TestCase
from unittest.mock import patch, call
from django.urls import reverse
from django.contrib.auth.models import User

from account.models import Profile


class UserViewTest(TestCase):

    def setUp(self) -> None:
        self.username = 'user_test'
        self.user_password = '!qa2ws3ED'
        self.user_email = 'test@gamil.com'
        self.user_first_name = 'test'

    def tearDown(self) -> None:
        pass

    def test_login(self):
        url = reverse('login')
        response = self.client.post(url,
                                    data={'username': self.username,
                                          'password': self.user_password})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_with_empty_username(self):
        url = reverse('login')
        response = self.client.post(url,
                                    data={'username': '',
                                          'password': self.user_password})

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_with_empty_password(self):
        url = reverse('login')
        response = self.client.post(url,
                                    data={'username': self.username,
                                          'password': ''})

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logout(self):
        url = reverse('logout')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'registration/logged_out.html')

    def test_register_GET(self):
        url = reverse('register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'account/template/register.html')

    def test_register_POST(self):
        url = reverse('register')
        response = self.client.post(url,
                                    data={'username': self.username,
                                          'first_name': self.user_first_name,
                                          'email': self.user_email,
                                          'password': self.user_password,
                                          'password2': self.user_password,
                                          })

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'account/template/register_done.html')


class EditTest(TestCase):

    def setUp(self) -> None:
        self.username = 'user_test'
        self.user_password = '!qa2ws3ED'
        self.user_email = 'test@gamil.com'
        self.user_first_name = 'test'
        self.user = User.objects.create(username=self.username,
                                        first_name=self.user_first_name,
                                        email=self.user_email,
                                        password=self.user_password,
                                        )
        self.profile = Profile.objects.create(user=self.user)

    def tearDown(self) -> None:
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_edit_GET(self):
        self.client.force_login(self.user)
        url = reverse('edit')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'account/user/edit.html')

    def test_edit_POST(self):
        self.client.force_login(self.user)
        user = User.objects.get()
        self.assertEqual(user.last_name, '', user)

        url = reverse('edit')
        last_name = 'last_name'
        response = self.client.post(url,
                                    data={'first_name': self.user_first_name,
                                          'last_name': last_name,
                                          'email': self.user_email,
                                          'date_of_birth': '',
                                          'photo': '',
                                          }
                                    )
        user = User.objects.get()

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'account/user/edit.html')
        self.assertEqual(user.last_name, last_name, user)

    def test_edit_POST_with_wrong_email(self):
        self.client.force_login(self.user)
        user = User.objects.get()
        self.assertEqual(user.email, self.user_email, user)

        url = reverse('edit')
        wrong_email = 'wrong_email@gmail'
        response = self.client.post(url,
                                    data={'first_name': self.user_first_name,
                                          'last_name': 'last_name',
                                          'email': wrong_email,
                                          'date_of_birth': '',
                                          'photo': '',
                                          }
                                    )
        user = User.objects.get()

        self.assertEqual(response.status_code, 200, response)
        self.assertTemplateUsed(response, 'account/user/edit.html')
        self.assertNotEqual(user.email, wrong_email, user)
