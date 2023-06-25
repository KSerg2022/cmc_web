from django.contrib import admin

from .models import Exchanger, ExPortfolio

from cmc.models import Cryptocurrency


@admin.register(Exchanger)
class ExchangerAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'host', 'url', 'prefix', 'is_active', 'logo', 'website')
    list_filter = ('name', 'is_active')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name', )


@admin.register(ExPortfolio)
class ExPortfolioAdmin(admin.ModelAdmin):
    list_display = ('exchanger', 'slug', 'api_key', 'api_secret', 'password',
                    'owner', 'comments')
    list_filter = ('exchanger', 'owner',)
    search_fields = ('exchanger', 'owner', 'currencies')
    prepopulated_fields = {'slug': ('owner', 'exchanger')}
    ordering = ('exchanger', 'owner')



