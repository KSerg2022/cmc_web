from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import validate_image_file_extension
from django.conf import settings


def validate_telegram(value):
    from django.core.exceptions import ValidationError
    import re
    pattern = re.compile(r'^(?:[a-zA-Z0-9_]{5,}$)')
    if not pattern.search(value):
        raise ValidationError("Telegram username not correct.")
    return value


class Profile(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True,
                              validators=[validate_image_file_extension]
                              )
    telegram = models.CharField(max_length=255,
                                verbose_name="telegram user's name",
                                unique=True,
                                null=True,
                                help_text='Example: after "@" -  nik',
                                blank=True,
                                validators=[validate_telegram])

    class Meta:
        ordering = ['owner']

    def __str__(self):
        return f'Profile of {self.owner.username}'
