from django.core.validators import validate_image_file_extension, validate_slug, URLValidator
from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse
from django.utils.text import slugify

from cmc.models import Cryptocurrency


class Exchanger(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Exchanger name',
                            unique=True,
                            help_text="50 characters max.",
                            error_messages={"required": "Please enter exchanger name"})
    slug = models.SlugField(max_length=50,
                            unique=True,
                            validators=[validate_slug])
    host = models.URLField(verbose_name='https://',
                           validators=[URLValidator])
    url = models.URLField(verbose_name='/url/',
                          blank=True)
    prefix = models.URLField(verbose_name='/url/',
                             blank=True)
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to=f'exchangers/%Y_%m_%d/',
                             blank=True,
                             validators=[validate_image_file_extension])

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
        return reverse('exchanger:detail',
                       args=[self.slug])


class ExPortfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CharField,
                              related_name='exchanger_created')
    exchanger = models.ForeignKey(Exchanger,
                                  on_delete=models.CASCADE,
                                  related_name='portfolio')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            validators=[validate_slug])
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    password = models.CharField(max_length=255,
                                blank=True)
    comments = models.TextField(blank=True)
    currencies = models.ManyToManyField(Cryptocurrency,
                                        related_name='portfolio_currency',
                                        blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['exchanger'])
        ]
        ordering = ['exchanger']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.owner.username + '-' + self.exchanger.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.owner.username.capitalize()} have {self.exchanger.name} portfolio'

    def get_absolute_url(self):
        return reverse('exchanger:portfolio_detail',
                       args=[
                           self.owner.id,
                           self.exchanger.name,
                           self.slug])
