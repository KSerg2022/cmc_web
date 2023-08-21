import json
from unittest import TestCase

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from account.api.serializers import UserSerializer, ProfileSerializer
from account.api.views import UserViewSet
from account.models import Profile


class UserBase(TestCase):
    def setUp(self) -> None:
        self.username = 'user_test'
        self.user_password = 'test_password'

        self.endpoint_list = 'user-list'
        self.endpoint_detail = 'user-detail'

    def tearDown(self) -> None:
        User.objects.all().delete()

    def create_users(self):
        self.user_1 = User.objects.create_user(username=self.username + '1',
                                               password=self.user_password + '1')
        self.user_2 = User.objects.create_user(username=self.username + '2',
                                               password=self.user_password + '2')
        self.user_3 = User.objects.create_user(username=self.username + '3',
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
    def setUp(self) -> None:
        super(UserApiTestCase, self).setUp()
        self.user_admin = User.objects.create_superuser(username='user_admin',
                                                        password='user_admin')
        self.client.force_login(user=self.user_admin)

    def test_get(self):
        self.create_users()
        url = reverse(self.endpoint_list)
        response = self.client.get(url)

        serializer_data = self.get_serializer_data(url,
                                                   user=[self.user_admin, self.user_1, self.user_2, self.user_3])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_search_username(self):
        self.create_users()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'search': 'user_test1'})
        serializer_data = self.get_serializer_data(url, user=[self.user_1])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    # def test_get_search_is_active(self):
    #     self.create_users()
    #     url = reverse(self.endpoint)
    #     response = self.client.get(url, data={'search': 'False'})
    #     serializer_data = self.get_serializer_data(url,
    #                                                user=[self.user_3])
    #     print(User.objects.all().values())
    #     print(serializer_data)
    #     print(response.data)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_is_active(self):
        self.create_users()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'is_active': 'False'})

        serializer_data = self.get_serializer_data(url, user=[self.user_3])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_name(self):
        self.create_users()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'username': 'user_test1'})
        serializer_data = self.get_serializer_data(url, user=[self.user_1])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_ordering_name(self):
        self.create_users()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'ordering': 'username'})

        serializer_data = self.get_serializer_data(url,
                                                   user=[self.user_admin, self.user_1, self.user_2, self.user_3]
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-username'})

        serializer_data = self.get_serializer_data(url,
                                                   user=[self.user_3, self.user_2, self.user_1, self.user_admin])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        self.assertEqual(1, User.objects.all().count())

        url = reverse(self.endpoint_list)
        data = {
            'username': self.username,
            'password': self.user_password,

        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
        self.assertEqual(2, User.objects.all().count())
        self.assertEqual(2, response.data['id'])

    def test_create_not_admin(self):
        self.assertEqual(1, User.objects.all().count())
        self.create_users()
        self.client.logout()
        self.client.force_login(user=self.user_1)
        self.assertEqual(4, User.objects.all().count())

        url = reverse(self.endpoint_list)
        data = {
            'username': self.username,
            'password': self.user_password,

        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, response.data)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)

        self.assertEqual(4, User.objects.all().count())

    def test_update(self):
        self.create_users()

        self.assertEqual(4, User.objects.all().count())
        self.assertEqual(2, self.user_1.id)

        url_for_update = reverse(self.endpoint_detail, args=(self.user_1.id,))
        data = {
            'username': self.username,
            'password': self.user_password,
            'email': 'chacke_test@test.com'
        }
        json_data = json.dumps(data)
        response = self.client.put(url_for_update, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(4, User.objects.all().count())

        self.user_1.refresh_from_db()
        self.assertEqual(2, self.user_1.id)
        self.assertEqual('chacke_test@test.com', self.user_1.email)

    def test_update_not_admin(self):
        self.create_users()
        self.client.logout()
        self.client.force_login(user=self.user_1)

        self.assertEqual(4, User.objects.all().count())
        self.assertEqual(2, self.user_1.id)

        url_for_update = reverse(self.endpoint_detail, args=(self.user_1.id,))
        data = {
            'username': self.username,
            'password': self.user_password,
            'email': 'chacke_test@test.com'
        }
        json_data = json.dumps(data)
        response = self.client.put(url_for_update, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.assertEqual(4, User.objects.all().count())

        self.user_1.refresh_from_db()
        self.assertEqual(2, self.user_1.id)
        self.assertEqual('', self.user_1.email)

    def test_delete(self):
        self.create_users()
        self.assertEqual(4, User.objects.all().count())

        url_for_update = reverse(self.endpoint_detail, args=(self.user_1.id, ))
        response = self.client.delete(url_for_update)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(3, User.objects.all().count())

    def test_delete_not_admin(self):
        self.create_users()
        self.client.logout()
        self.client.force_login(user=self.user_1)

        self.assertEqual(4, User.objects.all().count())

        url_for_update = reverse(self.endpoint_detail, args=(self.user_1.id, ))
        response = self.client.delete(url_for_update)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.assertEqual(4, User.objects.all().count())


class BlockchainSerializerTestCase(UserBase):

    def test_user_serializer(self):
        self.create_users()
        url = reverse(self.endpoint_list)
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
        self.user1 = User.objects.create_user(username=self.username + '1',
                                              password=self.user_password)
        self.user2 = User.objects.create_user(username=self.username + '2',
                                              password=self.user_password)
        self.admin = User.objects.create_superuser(username=self.username + '_admin',
                                                   password=self.user_password,
                                                   is_staff=True)

        self.profile_date_of_birth1 = '2001-01-01'
        self.profile_date_of_birth2 = '2002-02-02'
        self.profile_photo = '/data_for_test/black.jpg'

        self.endpoint_list = 'profile-list'
        self.endpoint_detail = 'profile-detail'

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


class UserPortfolioApiTestCase(APITestCase, UserPortfolioBase):

    def setUp(self) -> None:
        super(UserPortfolioApiTestCase, self).setUp()
        self.client.force_login(user=self.user1)

    def test_get(self):
        self.create_profile()
        url = reverse(self.endpoint_list)
        response = self.client.get(url)
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_search_username(self):
        self.create_profile()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'search': 'user_test1'})
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile1])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_search_date_of_birth(self):
        self.create_profile()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'search': '2001-01-01'})
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile1])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_username(self):
        self.create_profile()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'user__username': 'user_test2'})
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile2])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_date_of_birth(self):
        self.create_profile()
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'date_of_birth': '2002-02-02'})
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile2])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_ordering_username(self):
        self.create_profile()
        url = reverse(self.endpoint_list)
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
        url = reverse(self.endpoint_list)
        response = self.client.get(url, data={'ordering': 'date_of_birth'})
        serializer_data = self.get_serializer_data(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        response = self.client.get(url, data={'ordering': '-date_of_birth'})
        serializer_data = self.get_serializer_data(url,
                                                   profile=[self.profile2, self.profile1])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_create(self):
        self.assertEqual(0, Profile.objects.all().count())

        url = reverse(self.endpoint_list)
        data = {
            'user': self.user1.id,
            'date_of_birth': self.profile_date_of_birth1,
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
        self.assertEqual(1, Profile.objects.all().count())
        self.assertEqual(self.user1.id, response.data['user'])

    def test_create_not_user(self):
        self.assertEqual(0, Profile.objects.all().count())
        self.client.logout()
        self.client.force_login(user=self.user2)

        url = reverse(self.endpoint_list)
        data = {
            'user': 1,
            'date_of_birth': self.profile_date_of_birth1,
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
        self.assertEqual(1, Profile.objects.all().count())
        self.assertNotEqual(self.user1.id, response.data['user'])
        self.assertEqual(self.user2.id, response.data['user'])

    def test_update(self):
        self.create_profile()

        self.assertEqual(1, self.profile1.id)
        self.assertEqual(self.profile_date_of_birth1, self.profile1.date_of_birth)

        url_for_update = reverse(self.endpoint_detail, args=(self.profile1.id,))
        data = {
            'user': self.user1.id,
            'date_of_birth': self.profile_date_of_birth2,
        }
        json_data = json.dumps(data)
        response = self.client.put(url_for_update, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.profile1.refresh_from_db()
        self.assertEqual(1, self.profile1.id)
        self.assertEqual(self.profile_date_of_birth2, self.profile1.date_of_birth.isoformat())

    def test_update_not_user(self):
        self.create_profile()
        self.client.logout()
        self.client.force_login(user=self.user2)

        self.assertEqual(self.user1.id, self.profile1.user.id)
        self.assertEqual(self.profile_date_of_birth1, self.profile1.date_of_birth)

        url_for_update = reverse(self.endpoint_detail, args=(self.profile1.id,))
        data = {
            'user': 1,
            'date_of_birth': self.profile_date_of_birth2,
        }
        json_data = json.dumps(data)
        response = self.client.put(url_for_update, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)

        self.profile1.refresh_from_db()
        self.assertEqual(self.user1.id, self.profile1.user.id)
        self.assertEqual(self.profile_date_of_birth1, self.profile1.date_of_birth.isoformat())

    def test_update_not_user_but_is_staff(self):
        self.create_profile()
        self.client.logout()
        self.client.force_login(user=self.admin)

        self.assertEqual(self.user1.id, self.profile1.user.id)
        self.assertEqual(self.profile_date_of_birth1, self.profile1.date_of_birth)

        url_for_update = reverse(self.endpoint_detail, args=(self.profile1.id,))
        data = {
            'user': 1,
            'date_of_birth': self.profile_date_of_birth2,
        }
        json_data = json.dumps(data)
        response = self.client.put(url_for_update, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.profile1.refresh_from_db()
        self.assertEqual(self.user1.id, self.profile1.user.id)
        self.assertEqual(self.profile_date_of_birth2, self.profile1.date_of_birth.isoformat())

    def test_delete(self):
        self.create_profile()
        self.assertEqual(2, Profile.objects.all().count())

        url_for_update = reverse(self.endpoint_detail, args=(self.profile1.id, ))
        response = self.client.delete(url_for_update)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Profile.objects.all().count())

    def test_delete_not_user(self):
        self.create_profile()
        self.client.logout()
        self.client.force_login(user=self.user2)

        self.assertEqual(2, Profile.objects.all().count())

        url_for_update = reverse(self.endpoint_detail, args=(self.profile1.id, ))
        response = self.client.delete(url_for_update)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.assertEqual(2, Profile.objects.all().count())

    def test_delete_not_owner_but_is_staff(self):
        self.create_profile()
        self.client.logout()
        self.client.force_login(user=self.admin)

        self.assertEqual(2, Profile.objects.all().count())

        url_for_update = reverse(self.endpoint_detail, args=(self.profile1.id, ))
        response = self.client.delete(url_for_update)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Profile.objects.all().count())


class ProfileSerializerTestCase(UserPortfolioBase):

    def test_blockchain_portfolio_serializer(self):
        self.create_profile()
        url = reverse(self.endpoint_list)
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
