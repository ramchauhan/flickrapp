from django.contrib import admin

from .models import UserData

class UserDataAdmin(admin.ModelAdmin):
    search_fields = ["search_key"]
    list_display = ["search_key", "user_ip"]

admin.site.register(UserData, UserDataAdmin)
