from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date_of_birth', 'photo']
    raw_id_fields = ['owner']
