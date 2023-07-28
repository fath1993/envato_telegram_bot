from django.contrib import admin

from envato.models import ConfigSetting, EnvatoFile, EnvatoUserFile


@admin.register(EnvatoFile)
class EnvatoFileAdmin(admin.ModelAdmin):
    list_display = (
        'link',
        'file_is_downloadable',
        'created_at_display',
        'updated_at_display',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fields = (
        'link',
        'file',
        'created_at',
        'updated_at',
    )

    @admin.display(description='دانلود شده', empty_value='???')
    def file_is_downloadable(self, obj):
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


@admin.register(EnvatoUserFile)
class EnvatoUserFileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'file',
        'is_single_pay',
        'is_noticed',
    )

    fields = (
        'user',
        'file',
        'is_single_pay',
        'is_noticed',
    )


@admin.register(ConfigSetting)
class Admin(admin.ModelAdmin):
    list_display = (
        'sleep_time',
        # 'is_proxy_on',
        'envato_user',
        'envato_pass',
    )

    fields = (
        'sleep_time',
        # 'is_proxy_on',
        'envato_user',
        'envato_pass',
        'envato_cookie',
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)