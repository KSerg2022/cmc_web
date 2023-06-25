from django.contrib import admin

from .models import Blockchain
# from .models import Currencies
from .models import Portfolio

from cmc.models import Cryptocurrency


@admin.register(Blockchain)
class BlockchainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'host', 'is_active', 'logo', 'website', 'scan_site')
    list_filter = ('name', 'is_active')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name', )


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('owner', 'blockchain', 'slug', 'api_key', 'wallet', 'comments', 'currencies')
    list_filter = ('blockchain', 'owner')
    search_fields = ('blockchain', 'owner', )
    prepopulated_fields = {'slug': ('owner', 'blockchain')}
    ordering = ('blockchain', 'owner')

