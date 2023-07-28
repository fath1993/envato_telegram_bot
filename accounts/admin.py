from django.contrib import admin
from accounts.models import Profile


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

