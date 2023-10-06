from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['owner', 'telegram', 'date_of_birth', 'photo']
    raw_id_fields = ['owner']
    list_filter = ('owner', 'telegram')
    search_fields = ('owner', 'telegram')
    ordering = ('owner', 'date_of_birth')
