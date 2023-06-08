from django.contrib import admin

from .models import Cryptocurrency


@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'slug', 'name', 'site', 'contract')
    list_filter = ('symbol', 'name')
    search_fields = ('symbol', 'name')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name', 'symbol')

