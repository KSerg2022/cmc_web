from django.db import models
from django.urls import reverse


class Cryptocurrency(models.Model):
    symbol = models.CharField(max_length=25, verbose_name='Symbol')
    name = models.CharField(max_length=25, verbose_name='Name')
    slug = models.SlugField(max_length=250)
    cmc_id = models.IntegerField(verbose_name='ID in coinmarketcap.com', blank=True)
    site = models.URLField(max_length=200,
                           verbose_name='Site',
                           blank=True,
                           )
    contract = models.CharField(max_length=255, verbose_name='Contract', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['symbol']),
        ]
        ordering = ['name']

    def __str__(self):
        return f'{self.name}. {self.symbol}'

    # def get_absolute_url(self):
    #     return reverse('cmc:crypto_detail',
    #                    args=[self.slug])

