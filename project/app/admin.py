from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_login']