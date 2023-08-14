from django.contrib.auth.models import User
from rest_framework import serializers

from account.models import Profile


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = ['url', 'username', 'email', 'is_staff']
        fields = '__all__'


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

