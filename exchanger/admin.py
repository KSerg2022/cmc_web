from django.contrib import admin

from .models import Exchanger


@admin.register(Exchanger)
class ExchangerAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'host', 'url', 'prefix', 'is_active', 'logo')
    list_filter = ('name', 'is_active')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name', )

