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

    def tearDown(self) -> None:
        User.objects.all().delete()

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
        fields = ['profile', 'logentry', 'social_auth', 'exchanger_created', 'blockchain_created', 'id', 'password',
                  'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',
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
        self.telegram = '@telegram'

    def tearDown(self) -> None:
        Profile.objects.all().delete()
        User.objects.all().delete()

    def test_profile_create(self):
        profile = Profile.objects.create(owner=self.user)
        self.assertTrue(profile, profile)
        self.assertEqual(profile.owner, self.user, profile)

    def test_profile_create_with_data_of_birth(self):
        profile = Profile.objects.create(owner=self.user,
                                         date_of_birth=self.profile_date_of_birth)
        self.assertTrue(profile, profile)
        self.assertEqual(profile.date_of_birth, self.profile_date_of_birth, profile)

    def test_profile_create_with_invalid_format_data_of_birth(self):
        profile = Profile(owner=self.user,
                          date_of_birth='01.01.2001')
        with self.assertRaises(ValidationError):
            profile.full_clean()
            profile.save()

    def test_profile_create_with_photo(self):
        profile = Profile.objects.create(owner=self.user,
                                         photo=self.profile_photo)
        self.assertTrue(profile, profile)
        self.assertEqual(profile.photo, self.profile_photo, profile)

    def test_profile_create_with_invalid_format_photo(self):
        with self.assertRaises(ValidationError) as e:
            profile = Profile.objects.create(owner=self.user,
                                             photo='./data_for_test/text.txt')
            profile.full_clean()
            profile.save()

    def test_profile_create_with_telegram(self):
        profile = Profile.objects.create(owner=self.user,
                                         telegram=self.telegram)
        self.assertTrue(profile, profile)
        self.assertEqual(profile.telegram, self.telegram, profile)

    def test_profile_create_with_telegram_wrong_name(self):
        telegrams = ['rrr', 'rrr$%!', 'fsgafgDDDf!', 'asfgw56wF_п', 'q@asfgw56wF', 'asfgw56w F', 'a sfgw56w']
        for telegram in telegrams:
            with self.assertRaises(ValidationError) as e:
                profile = Profile.objects.create(owner=User.objects.create(username=telegram,
                                                                           password=telegram),
                                                 telegram=telegram)
                profile.full_clean()
                profile.save()
            self.assertIn('Telegram username not correct.', str(e.exception))

    def test_profile_print(self):
        profile = Profile.objects.create(owner=self.user)

        self.assertEqual(str(profile), f'Profile of {self.user.username}', profile)

    def test_profile_fields(self):
        fields = ['id', 'owner', 'date_of_birth', 'photo', 'telegram']
        profile = Profile.objects.create(owner=self.user)
        model_fields = [field.name for field in profile._meta.get_fields()]

        self.assertEqual(model_fields, fields, model_fields)
