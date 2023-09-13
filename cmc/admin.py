from django.contrib import admin

from .models import Cryptocurrency, TelegramBot


@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'slug', 'name', 'website', 'logo')
    list_filter = ('symbol', 'name')
    search_fields = ('symbol', 'name')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name', 'symbol')


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ('bot_name', 'username', 'bot_token', 'chat_id', 'hash_password')
