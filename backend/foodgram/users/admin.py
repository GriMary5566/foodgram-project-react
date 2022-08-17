from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow)
