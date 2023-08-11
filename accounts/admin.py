from django.contrib import admin
from accounts.models import Profile, UserRequestHistory


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'vip_expiry_date',
        'account_credit',
    )

    fields = (
        'user',
        'profile_pic',
        'vip_expiry_date',
        'account_credit',
    )


@admin.register(UserRequestHistory)
class UserRequestHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'file',
        'is_single_pay',
        'is_noticed',
        'created_at',
    )

    readonly_fields = (
        'created_at',
    )

    fields = (
        'user',
        'file',
        'is_single_pay',
        'is_noticed',
        'created_at',
    )

