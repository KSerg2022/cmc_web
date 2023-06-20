from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib import auth
# from django.contrib.auth.models import User

from account.models import Profile

User = auth.get_user_model()


class UserModelTest(TestCase):
    '''тест модели пользователя'''

    def setUp(self) -> None:
        self.username = 'user_test'
        self.user_password = 'test_password'

    def test_user_create(self):
        user = User.objects.create(username=self.username, password=self.user_password)
        self.assertTrue(user)

    def test_primary_key(self):
        user = User.objects.create(username=self.username, password=self.user_password)
        self.assertIn(str(user.pk), '1', user)

    def test_user_create_with_empty_username(self):
        with self.assertRaises(ValidationError):
            user = User.objects.create(username='', password=self.user_password)
            user.full_clean()
            user.save()

    def test_user_create_with_empty_password(self):
        with self.assertRaises(ValidationError):
            user = User.objects.create(username='self.username', password='')
            user.full_clean()
            user.save()

    def test_user_fields(self):
        fields = ['profile', 'logentry', 'exchanger_created', 'id', 'password', 'last_login', 'is_superuser',
                  'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',
                  'date_joined', 'groups', 'user_permissions']
        user = User.objects.create()
        model_fields = [field.name for field in user._meta.get_fields()]

        self.assertEqual(model_fields, fields, model_fields)


class ProfileModelTest(TestCase):
    def setUp(self) -> None:
        self.username = 'user_test'
        self.user_password = 'test_password'
        self.user = User.objects.create(username=self.username,
                                        password=self.user_password)
        self.profile_date_of_birth = '2001-01-01'
        self.profile_photo = './data_for_test/black.jpg'

    def test_profile_create(self):
        profile = Profile.objects.create(user=self.user)
        self.assertTrue(profile, profile)
        self.assertEqual(profile.user, self.user, profile)

    def test_profile_create_with_data_of_birth(self):
        profile = Profile.objects.create(user=self.user,
                                         date_of_birth=self.profile_date_of_birth)
        self.assertTrue(profile, profile)
        self.assertEqual(profile.date_of_birth, self.profile_date_of_birth, profile)

    def test_profile_create_with_invalid_format_data_of_birth(self):
        profile = Profile(user=self.user,
                          date_of_birth='01.01.2001')
        with self.assertRaises(ValidationError):
            profile.full_clean()
            profile.save()

    def test_profile_create_with_photo(self):
        profile = Profile.objects.create(user=self.user,
                                         photo=self.profile_photo)
        self.assertTrue(profile, profile)
        self.assertEqual(profile.photo, self.profile_photo, profile)

    def test_profile_create_with_invalid_format_photo(self):
        with self.assertRaises(ValidationError) as e:
            profile = Profile.objects.create(user=self.user,
                                             photo='./data_for_test/text.txt')
            profile.full_clean()
            profile.save()

    def test_profile_print(self):
        profile = Profile.objects.create(user=self.user)

        self.assertEqual(str(profile), f'Profile of {self.user.username}', profile)

    def test_profile_fields(self):
        fields = ['id', 'user', 'date_of_birth', 'photo']
        profile = Profile.objects.create(user=self.user)
        model_fields = [field.name for field in profile._meta.get_fields()]

        self.assertEqual(model_fields, fields, model_fields)
