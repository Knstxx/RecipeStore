from django.contrib import admin

from users.models import User, Subscribe


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'username']


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe)
