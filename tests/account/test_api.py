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
        self.endpoint = 'user-list'

    def tearDown(self) -> None:
        User.objects.all().delete()

    def create_users(self):
        self.user_1 = User.objects.create(username=self.username + '1',
                                          password=self.user_password + '1')
        self.user_2 = User.objects.create(username=self.username + '2',
                                          password=self.user_password + '2')
        self.user_3 = User.objects.create(username=self.username + '3',
                                          password=self.user_password + '3',
                                          is_active=False)

    def get_serializer_data(self, url, user=None):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)
        serializer_context = {'request': Request(request), }

        if user is None:
            return UserSerializer([self.user_1, self.user_2, self.user_3], many=True,
                                  context=serializer_context).data
        return UserSerializer([*user], many=True,
                              context=serializer_context).data


class UserApiTestCase(APITestCase, UserBase):

    def test_get(self):
        self.create_users()
        url = reverse(self.endpoint)
        response = self.client.get(url)

        serializer_data = self.get_serializer_data(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_search_username(self):
        self.create_users()
        url = reverse(self.endpoint)
        response = self.client.get(url, data={'search': 'user_test1'})
        serializer_data = self.get_serializer_data(url, user=[self.user_1])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    # def test_get_search_is_active(self):
    #     self.create_users()
    #     url = reverse(self.endpoint)
    #     response = self.client.get(url, data={'search': False})
    #     serializer_data = self.get_serializer_data(url,
    #                                                user=[self.user_3])
    #     print(serializer_data)
    #     print(response.data)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_is_active(self):
        self.create_users()
        url = reverse(self.endpoint)
        response = self.client.get(url, data={'is_active': 'False'})

        serializer_data = self.get_serializer_data(url, user=[self.user_3])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_name(self):
        self.create_users()
        url = reverse(self.endpoint)
        response = self.client.get(url, data={'username': 'user_test1'})
        serializer_data = self.get_serializer_data(url, user=[self.user_1])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_ordering_name(self):
        self.create_users()
        url = reverse(self.endpoint)
        response = self.client.get(url, data={'ordering': 'username'})

        serializer_data = self.get_serializer_data(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-username'})

        serializer_data = self.get_serializer_data(url,
                                                   user=[self.user_3, self.user_2, self.user_1])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])


class BlockchainSerializerTestCase(UserBase):

    def test_user_serializer(self):
        self.create_users()
        url = reverse('user-list')
        serializer_data = self.get_serializer_data(url,
                                                   user=[self.user_1, self.user_2])
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
        self.user1 = User.objects.create(username=self.username + '1',
                                         password=self.user_password)
        self.user2 = User.objects.create(username=self.username + '2',
                                         password=self.user_password)

        self.profile_date_of_birth1 = '2001-01-01'
        self.profile_date_of_birth2 = '2002-02-02'
        self.profile_photo = '/data_for_test/black.jpg'

        self.endpoint = 'profile-list'

    def tearDown(self) -> None:
        Profile.objects.all().delete()
        User.objects.all().delete()

    def create_profile(self):
        self.profile1 = Profile.objects.create(user=self.user1,
                                               date_of_birth=self.profile_date_of_birth1,
                                               photo=self.profile_photo)
        self.profile2 = Profile.objects.create(user=self.user2,
                                               date_of_birth=self.profile_date_of_birth2,
                                               photo=self.profile_photo)

    def get_serializer_data(self, url, profile=None):
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get(url)
        serializer_context = {'request': Request(request), }

        if profile is None:
            return ProfileSerializer([self.profile1, self.profile2], many=True,
                                     context=serializer_context).data
        return ProfileSerializer([*profile], many=True,
                                 context=serializer_context).data


class BlockchainPortfolioApiTestCase(APITestCase, UserPortfolioBase):

    def test_get(self):
        self.create_profile()
        url = reverse(self.endpoint)
        response = self.client.get(url)
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_search_username(self):
        self.create_profile()
        url = reverse(self.endpoint)
        response = self.client.get(url, data={'search': 'user_test1'})
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile1])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_search_date_of_birth(self):
        self.create_profile()
        url = reverse(self.endpoint)
        response = self.client.get(url, data={'search': '2001-01-01'})
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile1])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_username(self):
        self.create_profile()
        url = reverse(self.endpoint)
        response = self.client.get(url, data={'user__username': 'user_test2'})
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile2])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_date_of_birth(self):
        self.create_profile()
        url = reverse(self.endpoint)
        response = self.client.get(url, data={'date_of_birth': '2002-02-02'})
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile2])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_ordering_username(self):
        self.create_profile()
        url = reverse(self.endpoint)
        response = self.client.get(url, data={'ordering': 'user__username'})
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-user__username'})
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(serializer_data, response.data['results'])

    def test_get_ordering_date_of_birth(self):
        self.create_profile()
        url = reverse(self.endpoint)
        response = self.client.get(url, data={'ordering': 'date_of_birth'})
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-date_of_birth'})
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile2, self.profile1])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])


class ProfileSerializerTestCase(UserPortfolioBase):

    def test_blockchain_portfolio_serializer(self):
        self.create_profile()
        url = reverse('profile-list')
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile1])
        expected_data = [
            {
                'id': self.profile1.id,
                'date_of_birth': self.profile_date_of_birth1,
                'photo': 'http://testserver/media' + self.profile_photo,
                'user': self.user1.id,
            },
        ]

        self.assertEqual(expected_data, serializer_data)
