from django.contrib import admin

from envato.models import EnvatoFile, EnvatoActiveThread, EnvatoSetting, EnvatoTelegramBotSetting


@admin.register(EnvatoFile)
class EnvatoFileAdmin(admin.ModelAdmin):
    list_display = (
        'page_link',
        'src_link',
        'file_is_downloaded',
        'in_progress',
        'is_acceptable_file',
        'created_at_display',
        'updated_at_display',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fields = (
        'page_link',
        'src_link',
        'file',
        'in_progress',
        'is_acceptable_file',
        'created_at',
        'updated_at',
    )

    @admin.display(description='دانلود شده', empty_value='???')
    def file_is_downloaded(self, obj):
        if obj.file:
            return 'بله'
        else:
            return 'خیر'

    @admin.display(description='تاریخ ایجاد', empty_value='???')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    @admin.display(description='تاریخ بروزرسانی', empty_value='???')
    def updated_at_display(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M')


@admin.register(EnvatoSetting)
class EnvatoSettingAdmin(admin.ModelAdmin):
    list_display = (
        'sleep_time',
        'envato_user',
        'envato_pass',
        'login_status',
        'envato_thread_number',
        'envato_queue_number',
    )

    fields = (
        'sleep_time',
        # 'is_proxy_on',
        'envato_user',
        'envato_pass',
        'envato_cookie',
        'login_status',
        'envato_thread_number',
        'envato_queue_number',
    )


@admin.register(EnvatoTelegramBotSetting)
class EnvatoTelegramBotSettingAdmin(admin.ModelAdmin):
    list_display = (
        'bot_address',
        'bot_token',
    )

    fields = (
        'bot_address',
        'bot_token',
    )


@admin.register(EnvatoActiveThread)
class EnvatoActiveThreadAdmin(admin.ModelAdmin):
    list_display = (
        'id',
    )

    readonly_fields = (
        'id',
    )

    fields = (
        'id',
    )

    def has_add_permission(self, request):
        return False



