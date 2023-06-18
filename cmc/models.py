from django.core.validators import validate_image_file_extension
from django.db import models
from django.urls import reverse


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
