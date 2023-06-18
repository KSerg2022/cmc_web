from django.core.validators import validate_image_file_extension, validate_slug, URLValidator
from django.db import models


from django.urls import reverse
from django.utils.text import slugify


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
