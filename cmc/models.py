from django.core.validators import validate_image_file_extension
from django.db import models
from django.urls import reverse

from passlib.hash import pbkdf2_sha256


class Cryptocurrency(models.Model):
    symbol = models.CharField(max_length=255, verbose_name='Symbol')
    name = models.CharField(max_length=255, verbose_name='Name')
    slug = models.SlugField(max_length=250, unique=True)
    website = models.URLField(max_length=200,
                              verbose_name='Site',
                              blank=True,
                              )

    contract = models.CharField(max_length=255, verbose_name='Contract', blank=True)
    description = models.TextField(verbose_name='Description', blank=True)
    logo = models.ImageField(upload_to=f'cryptocurrency/%Y/%m/%d/',
                             blank=True,
                             validators=[validate_image_file_extension])

    class Meta:
        indexes = [
            models.Index(fields=['symbol']),
        ]
        ordering = ['name']

    def __str__(self):
        return f'{self.name}. {self.symbol}'

    def get_absolute_url(self):
        return reverse('cmc:crypto_detail',
                       args=[self.slug])


class TelegramBot(models.Model):
    bot_name = models.CharField(max_length=255,
                                unique=True,
                                verbose_name='bot_name',
                                help_text="Bot name from telegram bot settings.")
    username = models.CharField(max_length=255,
                                unique=True,
                                verbose_name='username',
                                help_text="Bot username from telegram bot settings.", )
    bot_token = models.CharField(max_length=255,
                                 unique=True,
                                 verbose_name='bot_token',
                                 help_text="Bot token from telegram bot settings.", )
    chat_id = models.IntegerField(unique=True,
                                  verbose_name='chat_id',
                                  help_text="Bot id.", )
    hash_password = models.CharField(max_length=255,
                                     unique=True, )

    class Meta:
        indexes = [
            models.Index(fields=['bot_name']),
        ]
        ordering = ['bot_name']

    def __str__(self):
        return f'{self.bot_name}.'

    def save(self, *args, **kwargs):
        self.hash_password = pbkdf2_sha256.hash(f'{self.bot_name} + {self.username} + {self.chat_id}')
        super().save(*args, **kwargs)


def pwd_verify(*args, **kwargs):
    bot_name, username, chat_id = args
    hash_password = TelegramBot.objects.first().hash_password
    return bool(pbkdf2_sha256.verify(f'{bot_name} + {username} + {chat_id}',
                                     hash_password))
