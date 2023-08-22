from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import validate_image_file_extension
from django.conf import settings


class Profile(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True,
                              validators=[validate_image_file_extension]
                              )

    class Meta:
        ordering = ['owner']

    def __str__(self):
        return f'Profile of {self.owner.username}'
