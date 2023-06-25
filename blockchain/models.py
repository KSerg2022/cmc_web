from django.core.validators import validate_image_file_extension, validate_slug, URLValidator
from django.db import models
from django.contrib.auth.models import User
import json

from django.urls import reverse
from django.utils.text import slugify

from cmc.models import Cryptocurrency


class Blockchain(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='blockchain name',
                            unique=True,
                            help_text="50 characters max.",
                            error_messages={"required": "Please enter blockchain name"})
    slug = models.SlugField(max_length=50,
                            unique=True,
                            validators=[validate_slug])
    host = models.URLField(verbose_name='https://',
                           blank=True,
                           validators=[URLValidator])
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to=f'blockchains/%Y_%m_%d/',
                             blank=True,
                             validators=[validate_image_file_extension])
    website = models.URLField(max_length=200,
                              verbose_name='Site',
                              blank=True,
                              )
    scan_site = models.URLField(max_length=200,
                                verbose_name='scan site',
                                blank=True,
                                )

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name.capitalize()

    def get_absolute_url(self):
        return reverse('blockchain:detail',
                       args=[self.slug])


class Portfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='blockchain_created')
    blockchain = models.ForeignKey(Blockchain,
                                   on_delete=models.CASCADE,
                                   related_name='portfolio_blockchain')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            validators=[validate_slug])
    api_key = models.CharField(max_length=255)
    wallet = models.CharField(max_length=255)
    comments = models.TextField(blank=True)
    currencies = models.JSONField(blank=True,
                                  null=True,
                                  encoder=json.JSONEncoder,
                                  decoder=json.JSONDecoder
                                  )

    class Meta:
        indexes = [
            models.Index(fields=['blockchain'])
        ]
        ordering = ['blockchain']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.owner.username + '-' + self.blockchain.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.owner.username.capitalize()} have {self.blockchain.name} portfolio'

    def get_absolute_url(self):
        return reverse('blockchain:portfolio_detail',
                       args=[
                           self.owner.id,
                           self.blockchain.name,
                           self.slug])
