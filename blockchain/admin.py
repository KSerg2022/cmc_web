from django.contrib import admin
from django.db import models
from django.forms import Textarea, CharField, TextInput
from django_json_widget.widgets import JSONEditorWidget


from .models import Blockchain
# from .models import Currencies
from .models import Portfolio

from cmc.models import Cryptocurrency


@admin.register(Blockchain)
class BlockchainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'host', 'api_key', 'is_active', 'logo', 'website', 'scan_site')
    list_filter = ('name', 'is_active')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name', )


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'blockchain', 'slug', 'wallet', 'comments')
    list_filter = ('blockchain', 'owner')
    search_fields = ('blockchain', 'owner', )
    prepopulated_fields = {'slug': ('owner', 'blockchain')}
    ordering = ('blockchain', 'owner')
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 50})},
        models.CharField: {'widget': TextInput(attrs={'size': '150'})},
    }
