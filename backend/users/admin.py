from django.contrib import admin

from users.models import User, Subscribe


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_filter = (
        'username',
        'email'
    )
    search_fields = (
        'username',
        'email'
    )


admin.site.register(User, UserAdmin)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subscription'
    )
    list_filter = (
        'user',
        'subscription'
    )


admin.site.register(Subscribe, SubscribeAdmin)
