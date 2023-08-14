from unittest import TestCase

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.api.serializers import UserSerializer, ProfileSerializer
from account.api.views import UserViewSet
from account.models import Profile


class UserBase(TestCase):
    def setUp(self) -> None:
        self.username = 'user_test'
        self.user_password = 'test_password'

    def tearDown(self) -> None:
        User.objects.all().delete()

    def create_users(self):
        self.user_1 = User.objects.create(username=self.username + '1',
                                          password=self.user_password + '1')
        self.user_2 = User.objects.create(username=self.username + '2',
                                          password=self.user_password + '2')

    def get_serializer_data(self, url):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)

        serializer_context = {'request': Request(request), }

        return UserSerializer([self.user_1, self.user_2], many=True,
                              context=serializer_context).data


class UserApiTestCase(APITestCase, UserBase):

    def test_get(self):
        self.create_users()
        url = reverse('user-list')
        response = self.client.get(url)

        serializer_data = self.get_serializer_data(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])


class BlockchainSerializerTestCase(UserBase):

    def test_user_serializer(self):
        self.create_users()
        url = reverse('user-list')
        serializer_data = self.get_serializer_data(url)
        expected_data = [
            {
                'id': self.user_1.id,
                "username": "user_test1",
                "first_name": '',
                "last_name": '',
                "email": '',
                "is_staff": False,
                "is_active": True,
            },
            {
                'id': self.user_2.id,
                "username": "user_test2",
                "first_name": '',
                "last_name": '',
                "email": '',
                "is_staff": False,
                "is_active": True,
            }
        ]

        self.assertEqual(expected_data, serializer_data)


class UserPortfolioBase(TestCase):

    def setUp(self) -> None:
        self.username = 'user_test'
        self.user_password = 'test_password'
        self.user = User.objects.create(username=self.username,
                                        password=self.user_password)

        self.profile_date_of_birth = '2001-01-01'
        self.profile_photo = '/data_for_test/black.jpg'

    def tearDown(self) -> None:
        User.objects.all().delete()
        Profile.objects.all().delete()

    def create_profile(self):
        self.profile = Profile.objects.create(user=self.user,
                                              date_of_birth=self.profile_date_of_birth,
                                              photo=self.profile_photo)

    def get_serializer_data(self, url):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)

        serializer_context = {'request': Request(request), }

        return ProfileSerializer([self.profile], many=True,
                                 context=serializer_context).data


class BlockchainPortfolioApiTestCase(APITestCase, UserPortfolioBase):

    def test_get(self):
        self.create_profile()
        url = reverse('profile-list')
        response = self.client.get(url)
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])


class ProfileSerializerTestCase(UserPortfolioBase):

    def test_blockchain_portfolio_serializer(self):
        self.create_profile()
        url = reverse('profile-list')
        serializer_data = self.get_serializer_data(url)
        expected_data = [
            {
                'id': self.profile.id,
                'date_of_birth': self.profile_date_of_birth,
                'photo': 'http://testserver/media' + self.profile_photo,
                'user': self.user.id,
            },
        ]

        self.assertEqual(expected_data, serializer_data)
