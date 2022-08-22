from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import EmailLoginUser, Follow


class EmailLoginUserAdmin(UserAdmin):
    list_display = ('email', 'username')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username')


admin.site.register(EmailLoginUser, EmailLoginUserAdmin)
admin.site.register(Follow)
